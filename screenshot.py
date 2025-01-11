from pyautogui import screenshot
from datetime import datetime

def screenshot():
    screen = screenshot()

    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"---> {file_name}")

    screen.save(f"{file_name}.png")
