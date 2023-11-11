import ctypes

import numpy as np
import numpy.ctypeslib as ctl
from fastapi import FastAPI

LEDS_PER_CHANNEL = 220

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
        data = np.zeros((LEDS_PER_CHANNEL * 16), dtype=np.int32)
        data[LEDS_PER_CHANNEL * string_num + light_num] = int(val, 16)
        led_dma(data, LEDS_PER_CHANNEL, 1)
        return {"status": 1}
    except:
        return {"status": 0}