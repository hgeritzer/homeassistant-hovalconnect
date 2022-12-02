"""Binary sensor platform for integration_blueprint."""
from dataclasses import dataclass
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import BINARY_SENSOR_DEVICE_CLASS, DEFAULT_NAME, DOMAIN, PATH_FAST
from .coordinator import HovalConnectDataUpdateCoordinator
from .entity import (
    HovalConnectEntity,
    HovalConnectEntityDescription,
    create_description,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up binary_sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []

    for i in range(1, 4):
        for description in HEATING_CIRCUIT_BINARY_SENSOR_TYPES:

            _description = create_description("0", "hk" + str(i), description)

            entity = HovalConnectBinarySensor(coordinator, _description)
            entities.append(entity)

    for i in range(1, 2):
        for description in BOILER_BINARY_SENSOR_TYPES:

            _description = create_description("0", "ww" + str(i), description)

            entity = HovalConnectBinarySensor(coordinator, _description)
            entities.append(entity)

    async_add_entities(entities)


@dataclass
class HovalConnectBinarySensorEntityDescription(
    HovalConnectEntityDescription, BinarySensorEntityDescription
):
    """Description of a Solarfocus binary sensor entity"""

    on_state: str = None


class HovalConnectBinarySensor(HovalConnectEntity, BinarySensorEntity):
    """Representation of a HovalConnect binary sensor entity."""

    # _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HovalConnectDataUpdateCoordinator,
        description: HovalConnectEntityDescription,
    ):
        """Class initialization."""
        super().__init__(coordinator=coordinator, description=description)

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        try:
            return (
                self.coordinator.data[self.entity_description.unit_name][
                    self.entity_description.path
                ][
                    f"{self.entity_description.function_name}_{self.entity_description.datapoint_name}"
                ]
                == 1
            )
        except:
            return False

        return self.coordinator.data.get("title", "") == "foo"


HEATING_CIRCUIT_BINARY_SENSOR_TYPES = [
    HovalConnectBinarySensorEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp2051",
        key="state_heatingcircuit_control",
        device_class=BinarySensorDeviceClass.RUNNING,
        on_state="1",
    ),
]

BOILER_BINARY_SENSOR_TYPES = [
    HovalConnectBinarySensorEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp2052",
        key="state_boiler_control",
        device_class=BinarySensorDeviceClass.RUNNING,
        on_state="1",
    ),
]
