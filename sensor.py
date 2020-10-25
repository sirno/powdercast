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
)
from .scrape import get_snow_heights

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, entry, async_add_entities, discovery_info=None):
    _LOGGER.info("Setup powder cast entries.")
    async def async_update_data():
        try:
            async with async_timeout.timeout(60):
                snow_height = await get_snow_height()
                return [
                    {
                        ATTR_DATE: k,
                        ATTR_SNOW_HEIGHT_BOT: v[0],
                        ATTR_SNOW_HEIGHT_MID: v[1],
                        ATTR_SNOW_HEIGHT_TOP: v[2],
                    }
                    for k, v in snow_height.items()
                ]
        except Exception as err:
            raise UpdateFailed(f"Error: {err}.")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="powder_cast_sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=30),
    )

    await coordinator.async_refresh()

    async_add_entities(
        PowderCastEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class PowderCastEntity(CoordinatorEntity, Entity):
    """Powder Cast sensor."""

    def __init__(self, coordinator, idx):
        """Initialize powder cast sensor."""
        super().__init__(coordinator)
        self.idx = idx

    @property
    def name(self):
        """Return the name of the powder cast sensor."""
        return "Powder Cast"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data[idx][ATTR_SNOW_HEIGHT_TOP]

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data is None:
            return None

        return {
            ATTR_DATE: self.coordinator.data[self.idx][ATTR_DATE],
            ATTR_SNOW_HEIGHT_BOT: self.coordinator.data[self.idx][ATTR_SNOW_HEIGHT_BOT],
            ATTR_SNOW_HEIGHT_MID: self.coordinator.data[self.idx][ATTR_SNOW_HEIGHT_MID],
        }
