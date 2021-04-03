""" Model for a single light """
from datetime import datetime

from homeassistant.core import HomeAssistant

from .constants import Constants
from .lego_controller import LegoController
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
import spidev
import random

DOMAIN = Constants.DOMAIN

lights = []
controller: None

def setup_platform(hass: HomeAssistant, config, add_entities, discovery_info=None):
    global lights
    global controller

    controller = LegoController(len(config['models']))

    for model_idx in range(0, len(config['models'])):
        model = config['models'][model_idx]
        model_name = model['name']
        for dev_idx in range(0, len(model['lights'])):
            device = model['lights'][dev_idx]
            device_type = (device.get('type') or "light").lower()
            device_max_brightness = int(device.get('brightness') or '255')
            if  device_type == 'light':
                light = LegoLight(hass, int(model_idx), int(device['id']), 
                        device['name'], model_name, 
                        device_max_brightness,
                        controller)
            if device_type == 'fireplace':
                light = LegoFireplace(hass, int(model_idx), int(device['id']), 
                        device['name'], model_name, 
                        device_max_brightness,
                        controller)
            lights.append(light)

    add_entities(lights, True)
    hass.states.set("lego.binding", "Loaded!")
    return True


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

    def turn_on(self):
        self.state = STATE_ON

    def turn_off(self):
        self.state = STATE_OFF

    def brightness(self):
        if self.is_on:
            return self._max_brightness
        return 0


class LegoAnimatedLight(LegoLight):
    def __init__(self, hass: HomeAssistant, 
            model_nr: int, light_id: int, 
            name: str, model_name: str,
            max_brightness: int,
            controller: LegoController):
        super().__init__(hass, model_nr, light_id, name, model_name, max_brightness, controller)
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

class LegoFireplace(LegoAnimatedLight):
    def animate(self):
        self._current_brightness = int((self._max_brightness / 3) + (random.random() * (self._max_brightness / 3)))
        
