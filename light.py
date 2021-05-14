""" Code that instantiates the appropriate objects to control the different lights """
from .constants import Constants
from .controller import LegoController
from .lego_light_entity import LegoLight
from .lego_fireplace_entity import LegoFireplace
from .lego_composite_light_entity import LegoCompositeLight
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
        node_nr = int(model.get('node'))
        for dev_idx in range(0, len(model['lights'])):
            device = model['lights'][dev_idx]
            device_type = (device.get('type') or "light").lower()
            device_name = device['name']

            if  device_type == 'light':
                device_max_brightness = int(device.get('brightness') or '255')
                device_channel = int(device['channel'])

                light = LegoLight(hass, 
                        node_nr,
                        model_name, 
                        device_channel, 
                        device_name, 
                        device_max_brightness,
                        controller)
            
            if device_type == 'fireplace':
                device_max_brightness = int(device.get('brightness') or '255')
                device_channel = int(device['channel'])

                light = LegoFireplace(hass, 
                        node_nr, 
                        model_name, 
                        device_channel, 
                        device_name, 
                        device_max_brightness,
                        controller)
            
            if device_type == 'composite':
                components = device.get('components')
                light = LegoCompositeLight(hass, 
                        node_nr, 
                        model_name, 
                        device['name'], 
                        components, 
                        controller)

            lights.append(light)

    add_entities(lights, True)
    hass.states.set("lego.binding", "Loaded!")
    return True
