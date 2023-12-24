import os
import sys
import time
import ctypes
import colorsys

import numpy as np
import numpy.ctypeslib as ctl


LEDS_PER_CHANNEL = 100

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]

data = np.zeros((220 * 16), dtype=np.int32)
led_dma(data, LEDS_PER_CHANNEL, 10)
time.sleep(.01)
