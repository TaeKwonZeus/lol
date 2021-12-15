import time
import cv2
import mss
import mss.tools
import numpy as np
from PIL import Image
from pynput.keyboard import Listener
from screeninfo import get_monitors


class Speedometer:
    def __init__(self):
        main_monitor = get_monitors()[0]
        self.prev_img = None
        self.screen_region = {'top': 0, 'left': 0, 'width': main_monitor.width, 'height': main_monitor.height}
        self.region = {'top': 0, 'left': 0, 'width': 0, 'height': 0}

    def start_listener(self, callback_queue):
        with Listener(on_press=lambda event: self.on_key_press(event, callback_queue=callback_queue),
                      on_release=self.on_key_release) as listener:
            listener.join()

    def select_region_of_interest(self):
        with mss.mss() as sct:
            # Grab the data
            screenshot = sct.grab(self.screen_region)
            img = Image.frombytes(
                'RGB',
                (screenshot.width, screenshot.height),
                screenshot.rgb,
            )

            r = cv2.selectROI(np.array(img))
            self.region = {'top': r[0], 'left': r[1], 'width': r[2], 'height': r[3]}
            print(self.region)

    def capture_region(self):
        with mss.mss() as sct:
            a = time.time()
            # Grab the data
            img = sct.grab(self.region)
            if img != self.prev_img:
                self.prev_img = img
            # compare
            b = time.time()
            print(b - a)

    def display_meter(self):
        """
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            screen.fill(0, 0, 0)"""

        return 'd'

    def on_key_press(self, key, callback_queue):
        key = key.char
        if key == 'b':
            self.select_region_of_interest()
        if key == 's':
            while True:
                self.capture_region()
        if key == 'd':
            callback_queue.put(self.display_meter)

    def on_key_release(self, key):
        pass
