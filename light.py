""" Model for a single light """
from datetime import datetime

from homeassistant.core import HomeAssistant

from .constants import Constants
from .lego_controller import LegoController
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
import spidev

DOMAIN = Constants.DOMAIN

lights = []
controller: None

def setup_platform(hass: HomeAssistant, config, add_entities, discovery_info=None):
    global lights
    global controller
    print("--- Hello from lego setup platform")

    controller = LegoController(len(config['models']))

    for model_idx in range(0, len(config['models'])):
        model = config['models'][model_idx]
        model_name = model['name']
        for dev_idx in range(0, len(model['lights'])):
            device = model['lights'][dev_idx]
            light = LegoLight(hass, int(model_idx), int(device['id']), device['name'], model_name, controller)
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
            controller: LegoController):

        self.controller = controller

        self.entity_id = "light.lego_{}_{}".format(model_name.lower(), name.lower().replace(" ", "_"))
        self._light_id = light_id
        self._name = name
        self._model_name = model_name
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

    def turn_on(self):
        self.state = STATE_ON

    def turn_off(self):
        self.state = STATE_OFF

    def brightness(self):
        if self.is_on:
            return 255
        return 0




