import subprocess
import time

SEGFAULT_PROCESS_RETURNCODE = -11

while True:
    try:
        subprocess.run(["python3", "cycle.py"],
                    check=True)
    except subprocess.CalledProcessError as err:
        if err.returncode == SEGFAULT_PROCESS_RETURNCODE:
            print(f"{time.time()}; probably segfaulted")
        else:
            print(f"{time.time()}; crashed for other reasons: {err.returncode}")
    else:
        print("ok")
