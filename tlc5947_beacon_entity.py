from .tlc5947_light_entity import Tlc5947Light
from .tlc5947_animated_light_entity import Tlc5947AnimatedLight
from .constants import Constants
from .controller import Tlc5947Controller
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

import random

class Tlc5947Beacon(Tlc5947AnimatedLight):
    def __init__(self, 
            hass: HomeAssistant, 
            node: int, 
            model_name: str,
            channel: int, 
            name: str, 
            max_brightness: int,
            controller: Tlc5947Controller):
        super().__init__(hass, node, model_name, channel, name, max_brightness, controller)
        self._count = 0
        self._brightness = max_brightness

    def animate(self):
        self._count = (self._count + 1) % 25
        self._current_brightness = self._brightness if self._count < 2 else 0

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS

        