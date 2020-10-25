"""Constants for Powder Cast integration."""
from datetime import timedelta

DOMAIN = "powder_cast"

SCAN_INTERVAL = timedelta(minutes=30)

ATTR_DATE = "date"
ATTR_SNOW_HEIGHT_BOT = "snow_height_bot"
ATTR_SNOW_HEIGHT_MID = "snow_height_mid"
ATTR_SNOW_HEIGHT_TOP = "snow_height_top"

CONF_LOCATIONS = "locations"