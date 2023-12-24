import os
import sys
import time
import ctypes
import colorsys
import math

import numpy as np
import numpy.ctypeslib as ctl


LEDS_PER_CHANNEL = 100

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]

def int_from_rgb(rgb):
    red = round(rgb[0] * 255)
    green = round(rgb[1] * 255)
    blue = round(rgb[2] * 255)
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint


def solid_red():
    return [0xff0000] * 220 * 16

def solid_huecycle():
    return [int_from_rgb(colorsys.hsv_to_rgb(time.time() % 20 / 20,1,0.1))] * 220 * 16

def sparkle_huecycle():
    # new numpy bitgenerator with constant seed
    rng = np.random.default_rng(seed=12345)
    # get random brightnesses which vary slowly over time for all lights
    base_brightnesses = rng.uniform(low=0.0, high=1.0, size=220 * 16)
    # offset by time
    brightnesses = (np.sin(base_brightnesses + time.time() / 1) + 1) / 2
    base_colors = rng.uniform(low=0.0, high=1.0, size=220 * 16)
    colors = base_colors + (time.time() / 20)
    return [int_from_rgb(colorsys.hsv_to_rgb(colors[i],1,brightnesses[i])) for i in range(220 * 16)] 
    

while True:
    data = [0x000000] * 220 * 16#ssparkle_huecycle()
    led_dma(np.array(data, dtype=np.int32), LEDS_PER_CHANNEL, 10)

