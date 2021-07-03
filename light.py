""" Code that instantiates the appropriate objects to control the different lights """
from .constants import Constants
from .controller import Tlc5947Controller
from .tlc5947_light_entity import Tlc5947Light
from .tlc5947_fireplace_entity import Tlc5947Fireplace
from .tlc5947_composite_light_entity import Tlc5947CompositeLight
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

    nodes_list = config['nodes']

    controller = Tlc5947Controller(len(nodes_list))

    for node_idx in range(0, len(nodes_list)):
        node = nodes_list[node_idx]
        node_name = node['name']
        node_nr = int(node.get('node'))
        for dev_idx in range(0, len(node['lights'])):
            device = node['lights'][dev_idx]
            device_type = (device.get('type') or "light").lower()
            device_name = device['name']

            if  device_type == 'light':
                device_max_brightness = max(int(device.get('brightness') or '100'), 100)
                device_channel = int(device['channel'])

                light = Tlc5947Light(hass, 
                        node_nr,
                        node_name, 
                        device_channel, 
                        device_name, 
                        device_max_brightness,
                        controller)
            
            if device_type == 'fireplace':
                device_max_brightness = int(device.get('brightness') or '100')
                device_channel = int(device['channel'])

                light = Tlc5947Fireplace(hass, 
                        node_nr, 
                        node_name, 
                        device_channel, 
                        device_name, 
                        device_max_brightness,
                        controller)
            
            if device_type == 'composite':
                components = device.get('components')
                light = Tlc5947CompositeLight(hass, 
                        node_nr, 
                        node_name, 
                        device['name'], 
                        components, 
                        controller)

            lights.append(light)

    add_entities(lights, True)
    return True
