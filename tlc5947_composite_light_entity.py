from .constants import Constants
from .controller import Tlc5947Controller
from .tlc5947_light_entity import Tlc5947Light, LightEntity
from datetime import datetime
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

class Tlc5947CompositeLight(Tlc5947Light):
    controller: Tlc5947Controller
    _state = STATE_OFF
    _components = []

    def __init__(self, 
            hass: HomeAssistant, 
            node: int,
            model_name: str,
            name: str, 
            components: list,
            controller: Tlc5947Controller):

        self.controller = controller

        self.entity_id = "light.tlc5947_{}_{}".format(model_name.lower(), name.lower().replace(" ", "_"))
        self._name = name
        self._model_name = model_name
        self._brightness = 100
        self.last_seen = datetime.now()

        # Instantiate component lights
        for component_idx in range (0, len(components)):
            component = components[component_idx]
            component_channel = int(component.get('channel'))
            component_max_brightness = int(component.get('brightness') or '100')

            component_light = Tlc5947ComponentLight(self, component_max_brightness)
            self.controller.set_light(node, component_channel, component_light)

    def updated(self):
        self.last_seen = datetime.now()
        self.schedule_update_ha_state()
        
    @property
    def is_animated(self):
        return False



class Tlc5947ComponentLight():
    """ Individual light """
    def __init__(self, 
            composite_light: Tlc5947CompositeLight, 
            _max_brightness: int):

        self._composite_light = composite_light
        self._max_brightness = _max_brightness

    @property
    def brightness(self):
        if self._composite_light.is_on:
            return int ((self._max_brightness * self._composite_light.brightness) / 100)
        return 0

    @property
    def is_animated(self):
        return False
