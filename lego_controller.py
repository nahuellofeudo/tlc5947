import spidev
from .constants import Constants
from .dummy_lego_light import DummyLegoLight
import threading

class LegoController:
    
    spi: spidev.SpiDev
    lights_state = []
    num_models: int
    lock: threading.Lock

    def __init__(self, num_models: int):
        self.lock = threading.Lock()

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 5000

        to_send = [0x01, 0x02, 0x03]
        self.spi.xfer(to_send)

        # create the arrays to store all the values of all the lights
        # By default populate the model with dummy lights

        self.num_models = num_models
        for model in range(0, num_models):
            controller_lights = []
            for light in range(0, 24):
                controller_lights.append(DummyLegoLight())
            
            self.lights_state.append(controller_lights)

    def set_light(self, model_nr: int, light_nr: int, light):
        self.lights_state[model_nr][light_nr] = light


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
            print("buffer: " + str(buffer))
            self.spi.xfer(buffer)
        finally:
            self.lock.release()
