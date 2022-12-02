"""Sensor platform for HovalConnect."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import Platform, TEMP_CELSIUS, TIME_HOURS


from .const import DOMAIN, PATH_FAST, PATH_NORMAL, CONF_HEATING_CIRCUIT, CONF_BOILER
from .coordinator import HovalConnectDataUpdateCoordinator
from .entity import (
    HovalConnectEntity,
    HovalConnectEntityDescription,
    create_description,
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # config_entry.data[CONF_HEATING_CIRCUIT] = 2

    entities = []

    for i in range(1, config_entry.options.get(CONF_HEATING_CIRCUIT, 1) + 1):
        # for i in range(1, 4):
        for description in HEATING_CIRCUIT_SENSOR_TYPES:

            _description = create_description("0", "hk" + str(i), description)

            entity = HovalConnectSensor(coordinator, _description)
            entities.append(entity)

    for i in range(1, config_entry.options.get(CONF_BOILER, 1) + 1):
        for description in BOILER_SENSOR_TYPES:

            _description = create_description("0", "ww" + str(i), description)

            entity = HovalConnectSensor(coordinator, _description)
            entities.append(entity)

    for i in range(1, 2):
        for description in SYSTEM_SENSOR_TYPES:

            _description = create_description("0", "bl" + str(i), description)

            entity = HovalConnectSensor(coordinator, _description)
            entities.append(entity)

    async_add_entities(entities)


class HovalConnectSensor(HovalConnectEntity, SensorEntity):
    """HovalConnect Sensor class."""

    def __init__(
        self,
        coordinator: HovalConnectDataUpdateCoordinator,
        description: HovalConnectEntityDescription,
    ):
        """Class initialization."""
        super().__init__(coordinator=coordinator, description=description)

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        # print(self.coordinator.data)
        try:
            return self.coordinator.data[self.entity_description.unit_name][
                self.entity_description.path
            ][
                f"{self.entity_description.function_name}_{self.entity_description.datapoint_name}"
            ]
        except:
            return "None"
        # return self.coordinator.data


HEATING_CIRCUIT_SENSOR_TYPES = [
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp0",
        key="outer_temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp1",
        key="room_temperature_current_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp1001",
        key="room_temperature_target_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        datapoint_name="dp2",
        path=PATH_FAST,
        key="flow_temperature_current_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp1002",
        key="flow_temperature_target_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp2051",
        key="state_heatingcircuit_control",
    ),
]

BOILER_SENSOR_TYPES = [
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp4",
        key="boiler_current_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp1004",
        key="boiler_target_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp2052",
        key="state_boiler_control",
    ),
]

SYSTEM_SENSOR_TYPES = [
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp2080",
        key="system_cycles",
        icon="mdi:counter",
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp2083",
        key="system_cycles_greater_50_percent",
        icon="mdi:counter",
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp2081",
        key="system_operating_hours",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:hours-24",
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp2082",
        key="system_operating_hours_greater_50_percent",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:hours-24",
    ),
    HovalConnectEntityDescription(
        path=PATH_NORMAL,
        datapoint_name="dp1007",
        key="system_temperature_target_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    HovalConnectEntityDescription(
        path=PATH_FAST,
        datapoint_name="dp7",
        key="system_temperature_current_state",
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
]
