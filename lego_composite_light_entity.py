from .constants import Constants
from .controller import LegoController
from .lego_light_entity import LegoLight, LightEntity
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

from datetime import datetime


class LegoCompositeLight(LightEntity):
    controller: LegoController
    _state = STATE_OFF
    _components = []

    def __init__(self, 
            hass: HomeAssistant, 
            node: int,
            model_name: str,
            name: str, 
            components: list,
            controller: LegoController):

        self.controller = controller

        self.entity_id = "light.lego_{}_{}".format(model_name.lower(), name.lower().replace(" ", "_"))
        self._name = name
        self._model_name = model_name
        self.last_seen = datetime.now()

        # Instantiate component lights
        for component_idx in range (0, len(components)):
            component = components[component_idx]
            component_channel = int(component.get('channel'))
            component_max_brightness = int(component.get('brightness') or '255')

            component_light = LegoComponentLight(self, component_max_brightness)
            self.controller.set_light(node, component_channel, component_light)

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




class LegoComponentLight():
    """ Individual light """
    def __init__(self, 
            composite_light: LegoCompositeLight, 
            _max_brightness: int):

        self._composite_light = composite_light
        self._max_brightness = _max_brightness

    def brightness(self):
        if self._composite_light.is_on:
            return self._max_brightness
        return 0

    @property
    def is_animated(self):
        return False
