import threading
import time
def test():
    for i in range(5):
        print(threading.current_thread().name, i)
        time.sleep(1)
if __name__ == '__main__':
    thread = threading.Thread(target=test())
    thread.start()

    for i in range(5):
        print(threading.current_thread().name, i)
        time.sleep(1)