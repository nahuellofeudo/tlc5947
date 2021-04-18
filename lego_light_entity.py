from .constants import Constants
from .controller import LegoController
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

from datetime import datetime


class LegoLight(LightEntity):
    controller: LegoController
    _state = STATE_OFF

    def __init__(self, hass: HomeAssistant, 
            model_nr: int, light_id: int, 
            name: str, model_name: str,
            max_brightness: int,
            controller: LegoController):

        self.controller = controller

        self.entity_id = "light.lego_{}_{}".format(model_name.lower(), name.lower().replace(" ", "_"))
        self._light_id = light_id
        self._name = name
        self._model_name = model_name
        self._max_brightness = max_brightness
        self.last_seen = datetime.now()
        self.controller.set_light(model_nr, light_id, self)

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
