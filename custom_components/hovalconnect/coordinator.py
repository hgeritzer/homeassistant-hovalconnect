"""Coordinator for HovalConnect integration"""

from datetime import timedelta
import logging
from pprint import pprint

# from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_SCAN_INTERVAL
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import CONF_PLANT_ID, DOMAIN
from .asynchovalconnectweb import HovalconnectWebSession

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


class HovalConnectDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""

        self._entry = config_entry

        self.api = HovalconnectWebSession(
            self._entry.data.get(CONF_USERNAME), self._entry.data.get(CONF_PASSWORD)
        )
        self.api.debug = False
        self.platforms = []

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=self._entry.options.get(CONF_SCAN_INTERVAL, 10)
            ),
        )

    async def _async_login(self):
        await self.api.login()
        await self.api.set_plant(self._entry.data.get(CONF_PLANT_ID))

    async def _async_update_data(self):
        """Update data via library."""
        try:
            if not self.api.logged_in:
                await self._async_login()

            response = await self.api.get_live_state()

            if response.status_code == 200:
                # pprint(response.json())
                return response.json()
            else:
                # TODO: move to asynchovalconnectweb
                self.api.logged_in = False
                raise UpdateFailed
        except Exception as exception:
            _LOGGER.exception(exception)
            raise UpdateFailed() from exception
