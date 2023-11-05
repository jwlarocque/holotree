import os
import sys
import time
import ctypes

import numpy as np
import numpy.ctypeslib as ctl


LEDS_PER_CHANNEL = 4

rpi_lib = ctypes.CDLL("./rpi/led_dma.so")
led_dma = rpi_lib.LED_DMA
led_dma.argtypes = [ctl.ndpointer(np.int32,flags='aligned,c_contiguous'),ctypes.c_int,ctypes.c_int]


if __name__ == "__main__":
    offset = 0
    counter = 0
    subprocess_times = []
    try:
        last_time = time.time()
        while True:
            time.sleep(.2)
            counter += 1
            # channel_colors = ",".join(["800000" if i % 4 == offset else "000000" for i in range(0, LEDS_PER_CHANNEL)])
            subprocess_start = time.time()
            # TODO: call so lib here
            data = ([0] * (LEDS_PER_CHANNEL - 1 - offset) + [0xff0000] + [0] * offset + [0]) * 16
            led_dma(np.array(data, dtype=np.int32), LEDS_PER_CHANNEL, 10)
            subprocess_times.append(time.time() - subprocess_start)
            now = time.time()
            if now - last_time > 10:
                print(f"{counter / 10} Hz, avg subprocess time: {sum(subprocess_times) / len(subprocess_times) if subprocess_times else 'NaN'}")
                subprocess_times = []
                counter = 0
                last_time = now
            offset = (offset + 1) % LEDS_PER_CHANNEL
    except KeyboardInterrupt:
        print("interrupted")
        rpi_lib.terminate(0)
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
