import os
import time

import requests
import cv2


N_STRINGS = 10
LIGHTS_PER_STRING = 100
DATA_DIR = "data"


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

perspective_num = 0
while os.path.exists(f'{DATA_DIR}/{perspective_num}'):
    perspective_num += 1
os.makedirs(f'{DATA_DIR}/{perspective_num}')

print(f"Capturing perspective {perspective_num}")
input("Press ENTER to continue...")
time.sleep(10)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("Capturing clean plate")

ret, clean_plate = cap.read()
cap.release()
if not ret:
    print("???")
cv2.imwrite(f'{DATA_DIR}/{perspective_num}/clean_plate.jpg', clean_plate)


for string_num in range(N_STRINGS):
    for light_num in range(LIGHTS_PER_STRING):
        print(f"Capturing string {string_num} light {light_num}")
        resp = requests.post(f"http://holotree.local:8000/set?string_num={string_num}&light_num={light_num}")
        if not resp.ok:
            print(f"Error setting light {light_num} on string {string_num}: {resp.text}")
            exit()
        time.sleep(0.1)
        # horrible hack to make sure the image buffer is empty (otherwise desyncs)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        img_path = f'{DATA_DIR}/{perspective_num}/{string_num}_{light_num}.jpg'
        ret, img = cap.read()
        cap.release()
        cv2.imwrite(img_path, img)

resp = requests.post(f"http://holotree.local:8000/set?string_num=0&light_num=0&val=000000")
