# tlc5947

Custom component for home assistant to drive [Texas Instruments' TLC5947 24-channel PWM LED controller](https://www.ti.com/product/TLC5947) through a Raspberry Pi's SPI interface.

This component should drive any TLC5947 board provided that it's wired correctly, but at this time it has only been tested on the [Adafruit 24-Channel 12-bit PWM LED Driver](https://www.adafruit.com/product/1429).

### Installation and usage

In order to use this component you will need to do three things:

1. Connect a TLC5947 to a Raspberry Pi (any model) running Home Assistant.
2. Install this custom component in Home Assistant.
3. Configure the custom component.

### 1. Connecting a TLC5947 to a Raspberry Pi 

All Raspberry Pi boards have a SPI port connected to their 40-pin GPIO headers. You just need to wire four pins (3 signals plus ground) to your TLC5947 board:

| SPI signal | Pin on Pi's GPIO header | Pin on TLC5947|
|-----|-----|-----|
|Data Out (MOSI) | 19  | Serial In (SIN) |
|Serial Clock (SCLK) | 23  | Clock (SCLK) |
|Chip Enable 0 (CE0)  | 24 | Latch (XLAT) | 
|Ground (GND)| 20 or any other GND pin (see [pinout](https://www.raspberrypi.org/documentation/usage/gpio/))| Ground (GND)|

\
Just in case, verify your board's [pinout](https://www.raspberrypi.org/documentation/usage/gpio/) in the official Raspberry Pi pinout page.

In addition to these pins, you will need to make sure that the TLC5947 has its own independent power supply. **DO NOT USE THE PI's 5V or 3.3V PINS TO POWER YOUR LEDs**. You risk blowing up the Pi's voltage regulator and/or your PSU.\
Instead, use a higher voltage (6V, 7.5V, 9V) and higher current PSU to drive the LEDs, and have that same PSU drive a regulator like [this one](https://www.amazon.com/gp/product/B071FJVRCT) to convert the voltage down to 5V for the Pi and the TLC5947's logic.

Controllers can be daisy-chained by wiring all Clock and Latch signals together, and connecting one controller's Data Out pin to the next one's Data In as explained in [the TLC5947's data sheet](https://www.ti.com/lit/ds/symlink/tlc5947.pdf). Most breakout boards have separate sets of pins for "input" and "output" to make this easier.

### 2. Installing the custom component in Home Assistant

Installing the component is easy: just clone the Git repository into your Home Assistant's custom_components directory (for example, /etc/home-assistant/custom_components if you are running the containerized version, or ~/.home-assistant/custom_components otherwise).

> $ cd $YOUR_HOME_ASSISTANT_CONFIGURATION_DIRECTORY \
> $ mkdir custom_components \
> $ cd custom_components \
> $ git clone https://github.com/nahuellofeudo/tlc5947.git


### 3. Configuring the component

The component needs to be configured through `configuration.yaml`. It does not support the GUI configuration flow (yet?).

The component supports:

- One or more cotrollers with 24 channels each. Each controller has an ID which represents the position in the daisy-chain, starting with 0. You can chain as many controllers as you want, as long as the signals don't degrade much.
- Up to 24 lights per controller, which can be controlled independently, grouped together, or animated (see below).

#### **Types of lights**

The current version of the component supports three types of light entities:

- **light**: Standard light entity that can be turned on or off. Each light can be given a fixed brightness in the range 0-255.
- **composite**: Groups multiple channels into a single light entity. Each channel can be given its own brightness level.
- **fireplace**: A light that changes intensity around 5 times per second within a hard-coded range. I created it to simulate the animation of a small fireplace in a personal project.

There is also an **AnimatedLight** base class that can be extended to implement other types of lights that change over time. This class should be extended and cannot be used directly.

#### **Syntax**

Below is an example `configuration.yaml` that defines:

* Two daisy-chained controllers (two TLC5947 units).
* The first controller controls two lights (channels 0 and 1). 
  * The first light is slightly dimmer (brightness  = 150) than the second one (default brightness = 255)
* The second controller controls two channels (2 and 3) grouped as a single composite light entity.
  * The two channels of the composite light have different brightness levels.

Example: 

        light:
        - platform: tlc5947
            nodes:

            - node: 0
                name: First controller
                lights:

                - name: Light 1
                  type: light
                  channel: 0
                  brightness: 150
                    
                - name: Light 2
                  type: light
                  channel: 1

            - node: 1
                name: Second controller
                lights:

                - name: Composite Light
                  type: composite
                  components:
                  - channel: 2
                    brightness: 100
                  - channel: 3
                    brightness: 120

