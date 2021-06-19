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

class Tlc5947Fireplace(Tlc5947AnimatedLight):
    def animate(self):
        self._current_brightness = int((self._max_brightness / 3) + (random.random() * (self._max_brightness / 3)))
        