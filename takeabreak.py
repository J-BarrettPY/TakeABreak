from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from pynput import keyboard, mouse
import threading
import time
import sys

main_countdown = 7200  # Main countdown starting 2 hours
cooldown_countdown = 1800  # Cooldown countdown starting 30 minutes
lock = threading.Lock()

activity_flag = False  # Indicates any activity (mouse or keyboard)

def reset_countdowns():
    global main_countdown, cooldown_countdown
    main_countdown = 7200
    cooldown_countdown = 1800

def show_popup(message):
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Break Time")
    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
    msg.exec_()

def countdown():
    global main_countdown, cooldown_countdown, activity_flag
    while True:
        time.sleep(1)
        with lock:
            if activity_flag:
                cooldown_countdown = 1800
                main_countdown -= 1
                print(f"Main Countdown: {main_countdown}")
                if main_countdown <= 0:
                    reset_countdowns()
                    show_popup("It is time to take a break! Stretch your body and rest your eyes.")
            else:
                if main_countdown != 7200:
                    cooldown_countdown -= 1
                    print(f"Cooldown Countdown: {cooldown_countdown}")
                    if cooldown_countdown <= 0:
                        reset_countdowns()
                        print("Cooldown ended, resetting main countdown.")
            activity_flag = False

def on_activity():
    global activity_flag, cooldown_countdown
    with lock:
        activity_flag = True
        cooldown_countdown = 1800  # Reset cooldown each time there's activity


def on_move(x, y): on_activity()
def on_click(x, y, button, pressed): on_activity()
def on_scroll(x, y, dx, dy): on_activity()
def on_press(key): on_activity()

threading.Thread(target=countdown, daemon=True).start()

with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
