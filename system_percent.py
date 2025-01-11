import psutil
import GPUtil


def system_percent():
    cpu_percent = psutil.cpu_percent(interval=1)  
    print(f"CPU usage: {cpu_percent}%")
    print("------")


    memory = psutil.virtual_memory()

    print(f"Total RAM: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Free RAM: {memory.free / (1024 ** 3):.2f} GB")
    print(f"Memory usage: {memory.percent}%")

    print("------")

    gpus = GPUtil.getGPUs()

    for gpu in gpus:
        print(f"GPU: {gpu.name}")
        print(f"GPU Memory Total: {gpu.memoryTotal} MB")
        print(f"GPU Memory Used: {gpu.memoryUsed} MB")
        print(f"GPU Memory Free: {gpu.memoryFree} MB")
        print(f"GPU Memory Usage: {gpu.memoryUtil * 100}%")
        print(f"GPU Temperature: {gpu.temperature} °C")

