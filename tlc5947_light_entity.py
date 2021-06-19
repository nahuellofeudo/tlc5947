from .constants import Constants
from .controller import Tlc5947Controller
from datetime import datetime
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

class Tlc5947Light(LightEntity):
    controller: Tlc5947Controller
    _state = STATE_OFF

    def __init__(self, 
            hass: HomeAssistant, 
            node: int, 
            model_name: str,
            channel: int,
            name: str, 
            max_brightness: int,
            controller: Tlc5947Controller):

        self.controller = controller

        self.entity_id = "light.tlc5947_{}_{}".format(model_name.lower(), name.lower().replace(" ", "_"))
        self._channel = channel
        self._name = name
        self._model_name = model_name
        self._max_brightness = max_brightness
        self.last_seen = datetime.now()
        self.controller.set_light(node, channel, self)

    def updated(self):
        self.last_seen = datetime.now()
        self.schedule_update_ha_state()
        
    @property
    def unique_id(self):
        return self.entity_id

    @property
    def is_on(self):
        return (self.state == STATE_ON)

    @property
    def supported_features(self):
        return 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newstate):
        self._state = newstate
        self.controller.update()

    @property
    def name(self):
        return self._name

    @property
    def is_animated(self):
        return False
    
    @property
    def device_class(self):
        return ["switch"]

    def turn_on(self):
        self.state = STATE_ON

    def turn_off(self):
        self.state = STATE_OFF

    def brightness(self):
        if self.is_on:
            return self._max_brightness
        return 0
