from homeassistant.core import HomeAssistant
import pytest

async def test_automation_trigger(hass: HomeAssistant):
    """Test automation triggers correctly."""
    # Setup
    await hass.async_start()
    await async_setup_component(hass, "automation", {
        "automation": {
            "trigger": {
                "platform": "state",
                "entity_id": "light.test"
            },
            "action": {
                "service": "light.turn_on",
                "entity_id": "light.response"
            }
        }
    })

    # Test
    await hass.states.async_set("light.test", "on")
    await hass.async_block_till_done()
    
    assert hass.states.get("light.response").state == "on"