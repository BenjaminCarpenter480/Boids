


import queue
import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import boids_gen
from numpy.linalg import norm

PATH="/tmp/boids"

DOMAIN = boids_gen.DOMAIN






class Display():


    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        time.sleep(2)
        self.pipe = open(PATH, "r")
        self.data = queue.Queue()

    def update(self, i):
        self._update_axis()
        while self.data.qsize() == 0:
            self.empty_pipe()
        data = self.data.get()
        for boid in data.split(';')[:-1]:
            print(boid)
            b=boid[:-1].split(',')
            self.ax.quiver(float(b[0]),float(b[1]),float(b[2]),float(b[3]),
                        headlength=norm([float(b[2]),float(b[3])]) )
        # print("---------LOOPED----------") 
            
            
    def empty_pipe(self): 
        count = 0
        while self.pipe.readable() and count < 500:
            self.data.put(self.pipe.readline())
            count = count +1

    
    
    
    def _update_axis(self):
        self.ax.clear()
        self.ax.set_xlim([0.1, DOMAIN])
        self.ax.set_ylim([0.1, DOMAIN])
        self.ax.set_xbound([0.1, DOMAIN])
        self.ax.set_ybound([0.1, DOMAIN])

    def startup(self):

        ani = FuncAnimation(self.fig, self.update, blit=False, interval=0.001)
        plt.show(block=True)
   
if __name__ == "__main__":
    time.sleep(0.5)
    display = Display()
    display.startup() 