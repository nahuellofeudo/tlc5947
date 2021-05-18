import spidev
from .constants import Constants
from .lego_dummy_light_entity import DummyLegoLight
import threading
import logging
import time

class LegoController:
    
    spi: spidev.SpiDev
    lights_state = []
    animated_lights = []
    num_models: int
    lock: threading.Lock
    animation_thread: threading.Thread

    def __init__(self, num_models: int):
        self.lock = threading.Lock()
        self.animation_thread = threading.Thread(target = self.animate)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 100000

        # create the arrays to store all the values of all the lights
        # By default populate the model with dummy lights

        self.num_models = num_models
        for model in range(0, num_models):
            controller_lights = []
            for light in range(0, 24):
                controller_lights.append(DummyLegoLight())
            
            self.lights_state.append(controller_lights)
        
        self.animation_thread.start()

    def set_light(self, model_nr: int, light_nr: int, light):
        self.lights_state[model_nr][light_nr] = light
        if light.is_animated:
            self.animated_lights.append(light)


    def update(self):
        """ Output the new brightness of all lights"""
        self.lock.acquire()
        try:
            buffer = bytearray()

            for model_nr in range(self.num_models - 1, -1, -1):
                for light_nr in range(23, 0, -2):
                    # Lights are processed in pairs (23, 22), (21, 20), etc.
                    # So that 2 lights (8-bit brightness per light) -> 6 bytes (12 bits per light)
                    msl_value = self.lights_state[model_nr][light_nr].brightness() & 0xff
                    lsl_value = self.lights_state[model_nr][light_nr - 1].brightness() & 0xff
                    total_value = (msl_value*16) << 12 | (lsl_value * 16)

                    # Add the bytes to the buffer
                    buffer.append((total_value >> 16) & 0xff)
                    buffer.append((total_value >> 8) & 0xff)
                    buffer.append((total_value >> 0) & 0xff)
            print("sending: {} bytes: {}".format(len(buffer), buffer.hex()))
            self.spi.xfer2(buffer)
        finally:
            self.lock.release()

    def animate(self):
        while True:
            for animated_light in self.animated_lights:
                animated_light.animate()
            self.update()
            time.sleep(0.5)