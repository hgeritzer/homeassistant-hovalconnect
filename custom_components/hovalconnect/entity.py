"""HovalConnectEntity class."""
import copy
from dataclasses import dataclass

from homeassistant.const import ATTR_ATTRIBUTION, ATTR_ID
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntityDescription


from .const import ATTR_INTEGRATION, ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import HovalConnectDataUpdateCoordinator


@dataclass
class HovalConnectEntityDescription(SensorEntityDescription):
    """Description of a HovalConnect entity"""

    unit_name: str | None = None
    function_name: str | None = None
    path: str | None = None
    datapoint_name: str | None = None


def create_description(
    unit_name: str,
    function_name: str,
    description: HovalConnectEntityDescription,
) -> HovalConnectEntityDescription:
    """Create Description"""
    _description = copy.copy(description)
    _description.unit_name = unit_name
    _description.function_name = function_name

    return _description


class HovalConnectEntity(CoordinatorEntity):
    """HovalConnectEntity entity."""

    def __init__(
        self,
        coordinator: HovalConnectDataUpdateCoordinator,
        description: HovalConnectEntityDescription,
    ):
        """Class initialization."""
        super().__init__(coordinator)
        self.entity_description = description

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        unique_id = f"{DOMAIN}_{self.entity_description.unit_name}_{self.entity_description.function_name}_{self.entity_description.datapoint_name}"
        return unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        _name = self.entity_description.key.replace("_", " ")
        return f"{self.entity_description.function_name.upper()} {_name}"

    @property
    def device_info(self) -> dict:
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator._entry.entry_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_ID: str(self.coordinator.data.get("id")),
            ATTR_INTEGRATION: DOMAIN,
        }
