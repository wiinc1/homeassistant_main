import logging
import os
import ssl
from functools import lru_cache
from pathlib import Path

import asyncio
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.config_entries import ConfigEntry
from homeassistant import core
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
)

from .const import (
    CONF_TOTP,
    CONF_KEY_ID,
    DOMAIN,
    WYZE_VAC_CLIENT,
    WYZE_VACUUMS,
    WYZE_USERNAME,
    WYZE_PASSWORD,
    CONF_POLLING,
    WYZE_SCAN_INTERVAL,
)

from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

_LOGGER = logging.getLogger(__name__)

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = ["vacuum", "switch", "camera", "sensor"]

# Optional sibling integration that may already hold valid tokens
_WYZEAPI_DOMAIN = "wyzeapi"
_ACCESS_TOKEN = "access_token"
_REFRESH_TOKEN = "refresh_token"


def _strip_cred(value: str | None) -> str | None:
    """Normalize credential strings (config UI paste often adds leading spaces)."""
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


@lru_cache(maxsize=1)
def _wyze_ca_bundle_path() -> str | None:
    """Return a CA bundle that trusts api.wyzecam.com (incomplete chain).

    api.wyzecam.com presents a leaf signed by DigiCert TLS RSA SHA256 2020 CA1
    but often omits that intermediate. certifi and even some system bundles
    then fail with CERTIFICATE_VERIFY_FAILED. We append the intermediate PEM
    shipped with this integration to the system CA bundle.
    """
    candidates = [
        ssl.get_default_verify_paths().cafile,
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
    ]
    system_ca = next((p for p in candidates if p and os.path.exists(p)), None)

    intermediate = Path(__file__).parent / "certs" / "DigiCertTLSRSASHA2562020CA1.pem"
    if not intermediate.is_file():
        _LOGGER.warning(
            "Missing intermediate CA %s; SSL to api.wyzecam.com may fail",
            intermediate,
        )
        return system_ca

    cache_dir = Path("/tmp/simple_wyze_vac")
    cache_dir.mkdir(parents=True, exist_ok=True)
    bundle = cache_dir / "ca_bundle.pem"

    parts: list[bytes] = []
    if system_ca:
        parts.append(Path(system_ca).read_bytes())
    parts.append(b"\n")
    parts.append(intermediate.read_bytes())
    bundle.write_bytes(b"".join(parts))
    _LOGGER.info("Built Wyze CA bundle at %s (system_ca=%s)", bundle, system_ca)
    return str(bundle)


@lru_cache(maxsize=1)
def _patch_wyze_sdk_ssl() -> str | None:
    """Force wyze_sdk requests sessions to use our CA bundle."""
    from wyze_sdk.service import base as wyze_base

    bundle = _wyze_ca_bundle_path()
    if bundle is None:
        _LOGGER.warning(
            "No CA bundle available; wyze_sdk will use certifi defaults"
        )
        return None

    original_do_request = wyze_base.BaseServiceClient._do_request

    def _do_request_with_system_ca(self, session, request):
        session.verify = bundle
        return original_do_request(self, session, request)

    wyze_base.BaseServiceClient._do_request = _do_request_with_system_ca
    _LOGGER.info("Routed wyze_sdk SSL verification through: %s", bundle)
    return bundle


def _create_client(
    username: str | None,
    password: str | None,
    key_id: str | None,
    api_key: str | None,
    totp: str | None,
    access_token: str | None = None,
    refresh_token: str | None = None,
) -> Client:
    """Create a Wyze Client using tokens if provided, else email login."""
    _patch_wyze_sdk_ssl()

    if access_token:
        client = Client(
            token=_strip_cred(access_token),
            refresh_token=_strip_cred(refresh_token),
        )
        # Proactively refresh if possible so expired access tokens recover
        if refresh_token:
            try:
                client.refresh_token()
                _LOGGER.info("Refreshed Wyze access token successfully")
            except Exception as err:  # noqa: BLE001 — try list anyway
                _LOGGER.debug("Token refresh skipped/failed: %s", err)
        return client

    return Client(
        None,
        None,
        _strip_cred(username),
        _strip_cred(password),
        _strip_cred(key_id),
        _strip_cred(api_key),
        _strip_cred(totp),
    )


def _tokens_from_wyzeapi(hass: core.HomeAssistant, username: str | None) -> tuple[str | None, str | None]:
    """Reuse tokens from a configured wyzeapi entry for the same account."""
    if not username:
        return None, None
    target = username.strip().lower()
    for entry in hass.config_entries.async_entries(_WYZEAPI_DOMAIN):
        entry_user = (entry.data.get(CONF_USERNAME) or "").strip().lower()
        if entry_user and entry_user != target:
            continue
        access = entry.data.get(_ACCESS_TOKEN)
        refresh = entry.data.get(_REFRESH_TOKEN)
        if access and refresh:
            _LOGGER.warning(
                "Email/API-key login failed; falling back to tokens from the "
                "wyzeapi integration for %s. Re-enter Simple Wyze Vac API keys "
                "when convenient.",
                username,
            )
            return access, refresh
    return None, None


async def async_setup_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Simple Wyze Vac from a config entry."""
    await hass.async_add_executor_job(_patch_wyze_sdk_ssl)

    username = _strip_cred(entry.data.get(CONF_USERNAME))
    password = _strip_cred(entry.data.get(CONF_PASSWORD))
    key_id = _strip_cred(entry.data.get(CONF_KEY_ID))
    api_key = _strip_cred(entry.data.get(CONF_API_KEY))
    totp = _strip_cred(entry.data.get(CONF_TOTP))

    # Persist stripped credentials so future loads / UI don't keep whitespace
    if any(
        (entry.data.get(k) or "") != (v or "")
        for k, v in (
            (CONF_USERNAME, username),
            (CONF_PASSWORD, password),
            (CONF_KEY_ID, key_id),
            (CONF_API_KEY, api_key),
            (CONF_TOTP, totp or ""),
        )
    ):
        new_data = {
            **entry.data,
            CONF_USERNAME: username,
            CONF_PASSWORD: password,
            CONF_KEY_ID: key_id,
            CONF_API_KEY: api_key,
            CONF_TOTP: totp or "",
        }
        hass.config_entries.async_update_entry(entry, data=new_data)
        _LOGGER.info("Normalized Simple Wyze Vac credentials (stripped whitespace)")

    client = None
    login_error: Exception | None = None
    try:
        client = await hass.async_add_executor_job(
            _create_client, username, password, key_id, api_key, totp
        )
        # Touch API so bad tokens fail here, not later mid-setup
        await hass.async_add_executor_job(client.vacuums.list)
    except Exception as err:  # noqa: BLE001
        login_error = err
        _LOGGER.warning("Wyze email/API-key login or device list failed: %s", err)
        client = None

    if client is None:
        access, refresh = _tokens_from_wyzeapi(hass, username)
        if access and refresh:
            try:
                client = await hass.async_add_executor_job(
                    _create_client,
                    None,
                    None,
                    None,
                    None,
                    None,
                    access,
                    refresh,
                )
                await hass.async_add_executor_job(client.vacuums.list)
                login_error = None
            except Exception as err:  # noqa: BLE001
                login_error = err
                client = None
                _LOGGER.error("Wyze token fallback also failed: %s", err)

    if client is None:
        msg = str(login_error) if login_error else "Unknown Wyze authentication error"
        # Credential problems should trigger reauth UI, not endless retries
        if any(
            x in msg.lower()
            for x in (
                "400",
                "invalid credentials",
                "1000",
                "auth",
                "password",
                "api key",
                "access token",
            )
        ):
            raise ConfigEntryAuthFailed(
                f"Wyze authentication failed: {msg}. "
                "Update username/password, regenerate Key ID + API Key at "
                "https://developer-api-console.wyze.com/, and reconfigure this integration."
            ) from login_error
        raise ConfigEntryNotReady(f"Unable to connect to Wyze: {msg}") from login_error

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    hass.data[WYZE_VACUUMS] = []

    hass.data[WYZE_USERNAME] = username
    hass.data[WYZE_PASSWORD] = password
    hass.data[CONF_KEY_ID] = key_id
    hass.data[CONF_API_KEY] = api_key
    hass.data[CONF_TOTP] = totp
    hass.data[CONF_POLLING] = entry.options.get(CONF_POLLING)
    hass.data[WYZE_SCAN_INTERVAL] = entry.options.get(CONF_SCAN_INTERVAL)

    try:
        device_list = await hass.async_add_executor_job(client.vacuums.list)
    except Exception as err:  # noqa: BLE001
        raise ConfigEntryNotReady(f"Failed to list Wyze vacuums: {err}") from err

    for device in device_list:
        _LOGGER.info(
            "Discovered Wyze device on account: %s with ID %s",
            username,
            device.mac,
        )

        vac_info = await hass.async_add_executor_job(
            lambda mac=device.mac: client.vacuums.info(device_mac=mac)
        )

        try:
            rooms = []
            maps = await hass.async_add_executor_job(
                lambda mac=device.mac: client.vacuums.get_maps(device_mac=mac)
            )
            room_manager = SWVRoomManager({})
            for map in maps:
                if map.rooms:
                    rooms = rooms + map.rooms
            room_manager = SWVRoomManager(rooms)

        except Exception as err:
            _LOGGER.warning(
                "Failed to query vacuum rooms. If your firmware is higher than "
                "1.6.113, rooms is currently not supported. Exception: %s",
                err,
            )
            room_manager = SWVRoomManager({})

        payload = {
            "mac": device.mac,
            "model": device.product.model,
            "name": device.nickname,
            "suction": vac_info.clean_level.describe(),
            "filter": vac_info.supplies.filter.remaining,
            "main_brush": vac_info.supplies.main_brush.remaining,
            "side_brush": vac_info.supplies.side_brush.remaining,
            "room_manager": room_manager,
            "battery": WyzeBattery(vac_info.voltage),
        }

        hass.data[WYZE_VACUUMS].append(payload)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def async_unload_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass, entry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


class SWVRoomManager:
    def __init__(self, rooms):
        self._rooms = {}
        for room in rooms:
            self._rooms[room.name] = True

    @property
    def rooms(self):
        return self._rooms

    def set(self, room_name):
        self._rooms[room_name] = True

    def clear(self, room_name):
        self._rooms[room_name] = False


class WyzeBattery:
    def __init__(self, value=0):
        self.value = value
