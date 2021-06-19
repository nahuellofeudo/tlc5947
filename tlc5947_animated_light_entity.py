from .tlc5947_light_entity import Tlc5947Light
from .constants import Constants
from .controller import Tlc5947Controller
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

class Tlc5947AnimatedLight(Tlc5947Light):
    def __init__(self, 
            hass: HomeAssistant, 
            node: int, 
            model_name: str,
            channel: int, 
            name: str, 
            max_brightness: int,
            controller: Tlc5947Controller):
        super().__init__(hass, node, model_name, channel, name, max_brightness, controller)
        self._current_brightness = 0

    def turn_on(self):
        self.state = STATE_ON

    def turn_off(self):
        self.state = STATE_OFF

    @property
    def is_animated(self):
        return True

    def brightness(self):
        if self.is_on:
            return self._current_brightness
        return 0

    def animate(self):
        pass