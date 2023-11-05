import ctypes

import numpy as np
import numpy.ctypeslib as ctl
from fastapi import FastAPI

LEDS_PER_CHANNEL = 4

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.post("/set")
def post_set(string_num:int, light_num:int, val:str="ff0000"):
    try:
        data = ([0] * light_num + [int(val, 16)] + [0] * (LEDS_PER_CHANNEL - 1 - light_num)) * 16
        # data = ([0] * (LEDS_PER_CHANNEL - 1 - light_num) + [int(val, 16)] + [0] * light_num + [0]) * 16
        led_dma(np.array(data, dtype=np.int32), LEDS_PER_CHANNEL, 10)
        return {"status": 1}
    except:
        return {"status": 0}