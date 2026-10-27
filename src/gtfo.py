import time
import random
import pydirectinput
import keyboard
import threading
import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import os
import sys

is_clicking = False

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

template_path = resource_path("auto_btn.png")
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

if template is None:
    print(f"[ERROR] File '{template_path}' not found!")
    print("Please take a screenshot of the dialog icon and save it next to the script")

def toggle_clicker(force_state=None):
    global is_clicking
    if force_state is not None:
        if is_clicking == force_state:
            return
        is_clicking = force_state
    else:
        is_clicking = not is_clicking
        
    if is_clicking:
        current_time = time.time()
        for btn in next_press_time:
            next_press_time[btn] = current_time

def is_button_on_screen(screenshot, template_img):
    if template_img is None:
        return False
        
    screen_np = np.array(screenshot)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
    
    h, w = screen_gray.shape
    search_zone = screen_gray[0:int(h*0.25), 0:int(w*0.25)]
    
    result = cv2.matchTemplate(search_zone, template_img, cv2.TM_CCOEFF_NORMED)
    
    _, max_val, _, _ = cv2.minMaxLoc(result)
    
    return max_val > 0.75

def listen_screen():
    while True:
        try:
            active_window = gw.getActiveWindow()
            
            if active_window and "Genshin Impact" in active_window.title:
                bbox = (active_window.left, active_window.top, active_window.right, active_window.bottom)
                screenshot = ImageGrab.grab(bbox=bbox)
                
                auto_button_visible = is_button_on_screen(screenshot, template)
                
                if auto_button_visible:
                    toggle_clicker(force_state=True)
                else:
                    toggle_clicker(force_state=False)
                
                time.sleep(0.15)
            else:
                time.sleep(0.5)
                
        except Exception as e:
            time.sleep(0.5)

threading.Thread(target=listen_screen, daemon=True).start()

print("Script launched successfully and is running AUTOMATICALLY")
print("To stop the script, close the console window")
print("The script does not work when the game is minimized")
print("In case of errors / if it stops working, restart the script")
print("The script tracks the dialog by the eye icon in the upper left. So do not hide the dialog interface!")

button_delays = {
    'f': (0.159, 0.226),
    'space': (0.176, 0.231),
    'left': (0.158, 0.228)
}

next_press_time = {btn: 0.0 for btn in button_delays}

try:
    while True:
        if is_clicking:
            active_window = gw.getActiveWindow()
            if active_window and "Genshin Impact" in active_window.title:
                current_time = time.time()
                
                for btn, delays in button_delays.items():
                    if current_time >= next_press_time[btn]:
                        if btn == 'left':
                            pydirectinput.click()
                        else:
                            pydirectinput.press(btn)
                        
                        random_delay = random.uniform(*delays)
                        next_press_time[btn] = current_time + random_delay
                
                time.sleep(0.02)
            else:
                time.sleep(0.2)
        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Script disabled")
