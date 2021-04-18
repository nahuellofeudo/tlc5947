""" Model for a single light """
from .constants import Constants
from .controller import LegoController
from .lego_light_entity import LegoLight
from .lego_fireplace_entity import LegoFireplace
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, Light
from homeassistant.const import STATE_UNAVAILABLE, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import EntityPlatform

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

