import os
import sys
import time
import ctypes
import colorsys
import json

import numpy as np
import numpy.ctypeslib as ctl


LEDS_PER_CHANNEL = 220
RADIANCE_DIST = 0.4
BOUNDS = [(-1, 1), (-1, 1), (0, 3)]
COLORS = [0x010000, 0x000100, 0x000001]

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]

xyz_dict = {}
with open("./xyz.json", "r") as f:
    xyz_dict = json.load(f)

def int_from_rgb(rgb):
    red = round(rgb[0] * 255)
    green = round(rgb[1] * 255)
    blue = round(rgb[2] * 255)
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

while True:
    start_time = time.time()
    while time.time() - start_time < 6:
        data = [0] * 220 * 16
        curr_time = time.time() - start_time
        axis = int(curr_time / 2) % 3
        direction = int(curr_time) % 2

        curr_min = BOUNDS[axis][0] - RADIANCE_DIST
        curr_max = BOUNDS[axis][1] + RADIANCE_DIST
        if direction == 1:
            curr_max, curr_min = curr_min, curr_max
        pos = (curr_max - curr_min) * (curr_time % 1) + curr_min
        # print(pos)
        for string_num in xyz_dict:
            for light_num in range(len(xyz_dict[string_num])):
                if xyz_dict[string_num][light_num]:
                    dist = abs(xyz_dict[string_num][light_num][axis] - pos)
                    if dist < RADIANCE_DIST:
                        data[LEDS_PER_CHANNEL * int(string_num) + light_num] += COLORS[axis] * int(255 * (1 - dist / RADIANCE_DIST) ** 3)
        led_dma(np.array(data, dtype=np.int32), 220, 10)
        # time.sleep(0.1)
    print("loop")


# all

# cube


while True:
    data = [int("000000", 16)] * 220 * 16
    target_height = (time.time() * 200) % 1200 + 100
    for string_num in xyz_dict:
        for light_num in range(len(xyz_dict[string_num])):
            if xyz_dict[string_num][light_num] and abs(xyz_dict[string_num][light_num][0] - target_height) < 100:
                data[LEDS_PER_CHANNEL * int(string_num) + light_num] += int("0f0000", 16)
            if xyz_dict[string_num][light_num] and abs(xyz_dict[string_num][light_num][1] - target_height) < 100:
                data[LEDS_PER_CHANNEL * int(string_num) + light_num] += int("000f00", 16)
            if xyz_dict[string_num][light_num] and abs(xyz_dict[string_num][light_num][2] - target_height) < 100:
                data[LEDS_PER_CHANNEL * int(string_num) + light_num] += int("00000f", 16)
            
    led_dma(np.array(data, dtype=np.int32), 220, 10)

# while True:
#     try:
#         data = [int_from_rgb(colorsys.hsv_to_rgb(time.time() % 20 / 20,1,0.1))] * 220 * 16
#         led_dma(np.array(data, dtype=np.int32), LEDS_PER_CHANNEL, 10)
#         time.sleep(.01)
#     except Exception as e:
#         print(e)
#         time.sleep(1)