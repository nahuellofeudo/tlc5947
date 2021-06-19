# tlc5947

Componente para home assistant para manejar [Controladores de LED de 24 canales TLC5947 de Texas Instruments](https://www.ti.com/product/TLC5947) a través del puerto SPI de una Raspberry Pi.

Este componente debería poder manejar cualquier placa basada en el TLC5947, pero de momento solamente está probado con el [Controlador de LED PWM de 24 canales de Adafruit](https://www.adafruit.com/product/1429).

### Instalación y uso

Para usar este componente vas a nacesitar hacer tres cosas:

1. Conectar un TLC5947 a una Raspberry Pi (cualquier modelo) que esté corriendo Home Assistant.
2. Instalar este componente en Home Assistant.
3. Configurar el componente.


### 1. Conectar el TLC5947 a una Raspberry Pi 

Todas las Raspberry Pi tienen un puerto SPI conectado al puerto GPIO de 40 pines. Solamente necesitás conectar 4 pines (3 señales y tierra) a la placa con el TLC5947:

| Señal SPI | Pin en el puerto GPIO | Pin del TLC5947|
|-----|-----|-----|
|Data Out (MOSI) | 19  | Serial In (SIN) |
|Serial Clock (SCLK) | 23  | Clock (SCLK) |
|Chip Enable 0 (CE0)  | 24 | Latch (XLAT) | 
|Tierra (GND)| 20 o cualquier otro pin GND (ver [pinout](https://www.raspberrypi.org/documentation/usage/gpio/))| Tierra (GND)|

\
Por las dudas, revisá el pinout de tu modelo de Pi en la [página oficial de pinouts](https://www.raspberrypi.org/documentation/usage/gpio/) de Raspberry Pi.

Además de estas 4 conexiones, los LEDs y el TLC5947 necesitan su propia alimentación independiente. **No uses los 5V o 3,3V de la Pi para alimentar los LEDs** porque corrés el riesgo de quemar los reguladores de la Pi.

En lugar de eso, usá una fuente de más voltaje (6, 7,5 ó 9 volts) y más corriente para alimentar los LEDs, y un regulador de voltaje [como este](https://www.amazon.com/gp/product/B071FJVRCT) para bajar la tensión a los 5V que necesuta la Pi y la lógica del TLC5947.

Los controladores se pueden encadenar unos a otros uniendo todas las señales de Clock y Latch, y conectando los pines de salida de un controlador a la entrada del siguiente como se muestra en la [hoja de datos del TLC5947](https://www.ti.com/lit/ds/symlink/tlc5947.pdf). 

### 2. Instalando el componente en Home Assistant

La instalación del componente de Home Assistant es muy fácil. Sólo hay que clonar el repositorio de Git dentro del directorio custom_components de Home Assistant (/etc/home-assistant/custom_components o ~/.home-assistant/custom_components dependiendo de cómo esté instalado).

> $ cd $YOUR_HOME_ASSISTANT_CONFIGURATION_DIRECTORY \
> $ mkdir custom_components \
> $ cd custom_components \
> $ git clone https://github.com/nahuellofeudo/tlc5947.git

### 3. Configuración del componente

El componente se debe configurar a través de `configuration.yaml` porque (todavía) no soporta configuración a través de la GUI.

El componente soporta:

- Uno o más controladores de 24 canales cada uno. Cada controlador tiene un identificador que representa su posición en la cadena de controladores, comenzando por el 0. Podés encadenar la cantidad de controladores que necesites, siempre y cuando las señales no se degraden demasiado.
- Hasta 24 luces por controlador, que se pueden controlar independientemente, agrupar o animar.

#### **Tipos de luces**

La versión actual de este componente soporta los siguientes tipos de luces:

- **light**: Entidad de luz estándar que se puede encender o apagar. A cada una se le puede asignar un valor de intensidad fijo en el rango 0-255.
- **composite**: Agrupa múltiples canales en el controlador en una única entidad de luz. Cada canal puede tener su propio valor de intensidad.
- **fireplace**: Una luz que cambia su intensidad alrededor de 5 veces por segundo dentro de un rango definido en el código. Creé este tipo de luz para simular un hogar a leña en un proyecto personal.

En el código también existe una clase **AnimatedLight** que sirve como clase base para otros tipos de luz animadas. Esta clase debe ser extendida por otras clases de entidades y no se puede usar directamente.

#### **Sintaxis**

Abajo se ve un ejemplo de `configuration.yaml` que define:

* Dos controladores (dos unidades TLC5947) encadenadas.
* El primer controlador controla dos luces (canales 0 y 1 respectivamente).
  * La primer luz es menos brillante (brightness  = 150) que la segunda (valor por defecto de brightness = 255).

* El segundo controlador controla dos canales (2 y 3) que son parte de una única entidad compuesta (composite).
  * Los dos canales que forman la entidad compuesta tienen diferentes valores de intensidad.

Ejemplo: 

        light:
        - platform: tlc5947
            nodes:

            - node: 0
                name: Primer controlador
                lights:

                - name: Luz 1
                  type: light
                  channel: 0
                  brightness: 150
                    
                - name: Luz 2
                  type: light
                  channel: 1

            - node: 1
                name: Segundo controlador
                lights:

                - name: Luz compuesta
                  type: composite
                  components:
                  - channel: 2
                    brightness: 100
                  - channel: 3
                    brightness: 120

