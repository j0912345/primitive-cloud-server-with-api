import sys
from subprocess import run as cmdRun
import threading
from time import sleep
use_cloud=True

# DAMN YOU OOP, SOMETHING LIKE THIS DOES <h1>NOT</h1> NEED TO BE A F***ING CLASS
# https://www.geeksforgeeks.org/how-to-create-a-new-thread-in-python/
class cmdTHREAD(threading.Thread):
    def __init__(self, command, thread_ID, shell_enabled=True):
        threading.Thread.__init__(self)
        self.command = command
        self.thread_ID = thread_ID
        self.shell_enabled = shell_enabled
    def run(self):
        return cmdRun(self.command, shell=self.shell_enabled)
 
#thread1 = cmdTHREAD("winver", 1000)
#thread2 = cmdTHREAD("cmd", 2000, False)
#thread1.start()
#thread2.start()

def start(python_port, javascript_port):
    javathread = cmdTHREAD(f"node ../primitive-cloud-server/src/index.js --python_port={python_port} --port={javascript_port}", 101)
    javathread.start()
    pythread=cmdTHREAD()
if __name__ == "__main__":
    argv = sys.argv
    print(len(argv))
    if len(argv) > 1:
        if argv[1] == "no_cloud":
            use_cloud=False
    start(8003, 8002)