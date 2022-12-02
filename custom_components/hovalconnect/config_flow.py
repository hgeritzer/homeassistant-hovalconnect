"""Adds config flow for HovalConnect."""
from typing import Optional

import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_PLANT_ID,
    DEFAULT_SCAN_INTERVAL,
    CONF_HEATING_CIRCUIT,
    CONF_BOILER,
)  # pylint: disable=unused-import


_LOGGER = logging.getLogger(__name__)


_COMPONENT_COUNT_ZERO_FOUR_SELECTOR = vol.All(
    selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0, max=4, mode=selector.NumberSelectorMode.SLIDER
        ),
    ),
    vol.Coerce(int),
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_PLANT_ID): cv.string,
        vol.Required(
            CONF_SCAN_INTERVAL,
            default=DEFAULT_SCAN_INTERVAL,
        ): cv.positive_int,
        vol.Required(
            CONF_HEATING_CIRCUIT,
            default=1,
        ): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
        vol.Required(CONF_BOILER, 1): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
    }
)

STEP_COMP_SELECTION_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_HEATING_CIRCUIT, default=1
        ): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
        vol.Optional(CONF_BOILER, default=1): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
    }
)


class HovalConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HovalConnect."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input: Optional[ConfigType] = None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #    return self.async_abort(reason="single_instance_allowed")  # noqa: E800

        _LOGGER.error("async_step_user")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if valid:

                data = dict(user_input)
                data.pop(CONF_SCAN_INTERVAL)
                data.pop(CONF_HEATING_CIRCUIT)
                data.pop(CONF_BOILER)

                options = dict(user_input)
                options.pop(CONF_USERNAME)
                options.pop(CONF_PASSWORD)
                options.pop(CONF_PLANT_ID)

                return self.async_create_entry(
                    title=user_input[CONF_PLANT_ID], data=data, options=options
                )

            self._errors["base"] = "auth"

        user_input = {}
        # Provide defaults for form
        # user_input[CONF_USERNAME] = self.data[CONF_USERNAME]
        # user_input[CONF_PASSWORD] = self.data[CONF_PASSWORD]
        # user_input[CONF_PLANT_ID] = self.data[CONF_PLANT_ID]

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """Get component options flow."""
        return HovalConnectOptionsFlowHandler(config_entry)

    # pylint: disable=unused-argument
    async def _show_config_form(self, user_input: Optional[ConfigType]):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=self._errors,
        )

    async def _test_credentials(self, username: str, password: str) -> bool:
        """Return true if credentials is valid."""
        try:
            # session = async_create_clientsession(self.hass)
            # client = IntegrationBlueprintApiClient(username, password, session)
            # await client.async_get_data()
            return True

        except Exception:  # pylint: disable=broad-except
            return False


class HovalConnectOptionsFlowHandler(config_entries.OptionsFlow):
    """HovalConnect config flow options handler."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize HovalConnect options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)
        self.errors = {}

    # pylint: disable=unused-argument
    async def async_step_init(self, user_input: Optional[ConfigType] = None):
        """Manage the options."""

        errors = {}

        if user_input is not None:
            print(f"OptionsFlow: going to update configuration {user_input}")

            # workaround to store into config_enty.data
            # self.hass.config_entries.async_update_entry(
            #    self.config_entry, data=user_input, options=self.config_entry.options
            # )
            # return self.async_create_entry(title="", data={})

            return self.async_create_entry(
                title=self.config_entry.data[CONF_PLANT_ID], data=user_input
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                    vol.Required(
                        CONF_HEATING_CIRCUIT,
                        default=self.options.get(CONF_HEATING_CIRCUIT, 1),
                    ): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
                    vol.Required(
                        CONF_BOILER, default=self.options.get(CONF_BOILER, 1)
                    ): _COMPONENT_COUNT_ZERO_FOUR_SELECTOR,
                }
            ),
            errors=errors,
        )
