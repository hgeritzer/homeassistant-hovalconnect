"""Constants for integration_blueprint."""

from typing import Final

from homeassistant.const import Platform

# Base component constants
NAME: Final = "HovalConnect"
DOMAIN: Final = "hovalconnect"
VERSION: Final = "0.1.0"
ATTRIBUTION: Final = ""
ISSUE_URL: Final = "https://github.com/hgeritzer/homeassistant-hovalconnect/issues"

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have ANY issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# Icons
ICON: Final = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS: Final = "connectivity"

# Platforms
PLATFORMS: Final = [
    Platform.SENSOR,
    # Platform.BINARY_SENSOR,
]

DEFAULT_SCAN_INTERVAL = 10

# Configuration and options
CONF_ENABLED: Final = "enabled"
CONF_PLANT_ID: Final = "plant_id"
CONF_HEATING_CIRCUIT = "heating_circuit"
CONF_BOILER = "boiler"

"""Configuration and options"""
CONF_HEATING_CIRCUIT = "heating_circuit"

PATH_FAST = "Fast"
PATH_NORMAL = "Normal"


# Defaults
DEFAULT_NAME: Final = DOMAIN

# Attributes
ATTR_INTEGRATION: Final = "integration"
