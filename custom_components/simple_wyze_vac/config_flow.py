import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.core import callback
from homeassistant import config_entries
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
)

from .const import (
    DOMAIN,
    CONF_POLLING,
    CONF_TOTP,
    CONF_KEY_ID,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=60)


def _strip(value: str | None) -> str:
    return (value or "").strip()


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_KEY_ID): str,
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_TOTP, default=""): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if self._async_current_entries():
                return self.async_abort(reason="already_configured")

            user_input = {
                CONF_USERNAME: _strip(user_input[CONF_USERNAME]),
                CONF_PASSWORD: _strip(user_input[CONF_PASSWORD]),
                CONF_KEY_ID: _strip(user_input[CONF_KEY_ID]),
                CONF_API_KEY: _strip(user_input[CONF_API_KEY]),
                CONF_TOTP: _strip(user_input.get(CONF_TOTP)),
            }

            try:
                from . import _create_client

                totp = user_input[CONF_TOTP] or None
                client = await self.hass.async_add_executor_job(
                    _create_client,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_KEY_ID],
                    user_input[CONF_API_KEY],
                    totp,
                )
                # Validate API works (SSL + credentials)
                await self.hass.async_add_executor_job(client.vacuums.list)
                return self.async_create_entry(
                    title="Simple Wyze Vac", data=user_input
                )
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Failed to login to Wyze servers")
                errors["base"] = "auth_error"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(self, entry_data):
        """Handle reauth when credentials stop working."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        errors = {}
        entry = getattr(self, "_reauth_entry", None)
        if entry is None:
            return self.async_abort(reason="reauth_successful")

        if user_input is not None:
            user_input = {
                CONF_USERNAME: _strip(user_input[CONF_USERNAME]),
                CONF_PASSWORD: _strip(user_input[CONF_PASSWORD]),
                CONF_KEY_ID: _strip(user_input[CONF_KEY_ID]),
                CONF_API_KEY: _strip(user_input[CONF_API_KEY]),
                CONF_TOTP: _strip(user_input.get(CONF_TOTP)),
            }
            try:
                from . import _create_client

                totp = user_input[CONF_TOTP] or None
                client = await self.hass.async_add_executor_job(
                    _create_client,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_KEY_ID],
                    user_input[CONF_API_KEY],
                    totp,
                )
                await self.hass.async_add_executor_job(client.vacuums.list)
                self.hass.config_entries.async_update_entry(entry, data=user_input)
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Reauth failed")
                errors["base"] = "auth_error"

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_USERNAME,
                    default=entry.data.get(CONF_USERNAME, ""),
                ): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(
                    CONF_KEY_ID, default=_strip(entry.data.get(CONF_KEY_ID))
                ): str,
                vol.Required(
                    CONF_API_KEY, default=_strip(entry.data.get(CONF_API_KEY))
                ): str,
                vol.Optional(
                    CONF_TOTP, default=_strip(entry.data.get(CONF_TOTP))
                ): str,
            }
        )
        return self.async_show_form(
            step_id="reauth_confirm", data_schema=schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="Simple Wyze Vac", data=user_input)

        if self._config_entry.options.get(CONF_POLLING):
            poll_default = self._config_entry.options.get(CONF_POLLING)
        else:
            poll_default = False

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_POLLING, default=poll_default): bool,
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self._config_entry.options.get(CONF_SCAN_INTERVAL),
                    ): str,
                }
            ),
        )
