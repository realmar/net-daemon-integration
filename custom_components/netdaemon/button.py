"""Button platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity

from .const import (
    ATTR_CLIENT,
    ATTR_COORDINATOR,
    ATTR_ENTITY_ID,
    DOMAIN,
    LOGGER,
    PLATFORM_BUTTON,
)
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup button platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN][ATTR_CLIENT]
    coordinator: "DataUpdateCoordinator" = hass.data[DOMAIN][ATTR_COORDINATOR]

    buttons = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_BUTTON:
            LOGGER.debug("Adding %s", entity)
            buttons.append(
              NetDaemonButton(coordinator, entity.split(".")[1])
            )

    if buttons:
        async_add_devices(buttons)


class NetDaemonButton(NetDaemonEntity, ButtonEntity):
    """NetDaemon Button class."""

    async def async_press(self) -> None:
        """Press the button."""
        await self._press()

    async def _press(self) -> None:
      """Press the button."""
      await self.hass.data[DOMAIN][ATTR_CLIENT].entity_update(
          {ATTR_ENTITY_ID: self.entity_id}
      )
      self.async_write_ha_state()
