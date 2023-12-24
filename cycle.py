import os
import sys
import time
import ctypes
import colorsys
import math
import json
import importlib

import numpy as np
import numpy.ctypeslib as ctl


LEDS_PER_CHANNEL = 220
PHASE_DURATION = 30
FADE_DURATION = 2
ANIMATIONS_DIR = "animations"
ENABLED = ["twinkle"]#["twinkle", "snow", "mom", "dad", "scan", "fireworks"]

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]

xyz_dict = {}
with open("xyz.json", "r") as f:
    xyz_dict = json.load(f)
xyz_combined = []
string_light_nums = []
for string_num in xyz_dict.keys():
    for light_num in range(len(xyz_dict[string_num])):
        if xyz_dict[string_num][light_num] is not None:
            coords = xyz_dict[string_num][light_num]
            xyz_combined.append((coords[0], coords[1], 3 - coords[2]))
            string_light_nums.append(LEDS_PER_CHANNEL * int(string_num) + light_num)

frame_generators = []
for file in os.listdir(ANIMATIONS_DIR):
    if file.endswith(".py"):
        module = importlib.import_module(f"{ANIMATIONS_DIR}.{file[:-3]}")
        if getattr(module, "ID", None) in ENABLED:
            print(file)
            frame_generators.append(module.FrameGenerator(np.array(xyz_combined)))
print(len(frame_generators))

# generator = frame_generators[0](np.array(xyz_combined))

while True:
    curr_time = time.time()
    current_generator_i = int(curr_time / PHASE_DURATION) % len(frame_generators)
    frame = frame_generators[current_generator_i].get_frame()
    fade_position = min(abs(((curr_time + FADE_DURATION) % PHASE_DURATION) - FADE_DURATION) / FADE_DURATION, 1)
    fade_factor = (1 - math.cos(fade_position * math.pi)) / 2
    data = [0] * 220 * 16
    for i in range(len(frame)):
        data[string_light_nums[i]] = 0x010000 * int(255 * frame[i][0] * fade_factor) + 0x000100 * int(200 * frame[i][1] * fade_factor) + 0x000001 * int(200 * frame[i][2] * fade_factor)
    led_dma(np.array(data, dtype=np.int32), LEDS_PER_CHANNEL, 10)