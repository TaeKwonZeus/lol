import queue
import threading
import pygame
import speedometer

# somewhere accessible to both:
callback_queue = queue.Queue()


def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)


def from_main_thread_blocking():
    callback = callback_queue.get()  # blocks until an item is available
    if 'd' == callback():
        print(threading.current_thread())
        screen = pygame.display.set_mode((200, 200))


def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False)  # doesn't block
        except queue.Empty:  # raised when queue is empty
            break
        callback()


sp = speedometer.Speedometer()

threading.Thread(target=sp.start_listener, args=(callback_queue,)).start()

while True:
    from_main_thread_blocking()
