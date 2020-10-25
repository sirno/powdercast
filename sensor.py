import async_timeout
import logging
from datetime import timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    UpdateFailed,
    DataUpdateCoordinator,
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    ATTR_DATE,
    ATTR_SNOW_HEIGHT_BOT,
    ATTR_SNOW_HEIGHT_MID,
    ATTR_SNOW_HEIGHT_TOP,
    CONF_LOCATIONS,
)
from .scrape import get_snow_heights

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.info("Setup powder cast entries.")

    locations = config.get(CONF_LOCATIONS)

    async_add_entities(PowderCastEntity(location) for location in locations)


class PowderCastEntity(Entity):
    """Powder Cast sensor."""

    def __init__(self, location):
        """Initialize powder cast sensor."""
        self.location = location
        self._data = None

    @property
    def name(self):
        """Return the name of the powder cast sensor."""
        return f"powder_cast_{self.location}"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._data is None:
            return None
        return self.coordinator.data[0][ATTR_DATE]

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "location": self.location,
            "forecast": self._data,
        }

    async def async_update(self):
        """Poll data from WePowder."""
        try:
            async with async_timeout.timeout(60):
                self._data = await get_snow_heights(self.location)
                return [
                    {
                        ATTR_DATE: k,
                        ATTR_SNOW_HEIGHT_BOT: v[2],
                        ATTR_SNOW_HEIGHT_MID: v[1],
                        ATTR_SNOW_HEIGHT_TOP: v[0],
                    }
                    for k, v in snow_height.items()
                ]
        except Exception as err:
            raise UpdateFailed(f"Error: {err}.")