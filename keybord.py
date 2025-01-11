import time
import keyboard
import threading

def log_keys(duration, output_file):
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

log_duration = 10 
output_file_path = "output_typed_text.txt"

log_keys(log_duration, output_file_path)
