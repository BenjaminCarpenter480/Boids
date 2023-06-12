


import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import boids_gen
from numpy.linalg import norm

PATH="/tmp/boids"

DOMAIN = boids_gen.DOMAIN






class Display():

    self.buffer = []

    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        time.sleep(2)
        self.pipe = open(PATH, "r")        


    def update(self, i):
        self._update_axis()

        data = self.pipe.readline()
        print(data.split(';')[:-1])
        for boid in data.split(';')[:-1]:
            print(boid)
            b=boid[:-1].split(',')
            self.ax.quiver(float(b[0]),float(b[1]),float(b[2]),float(b[3]),
                        headlength=norm([float(b[2]),float(b[3])]) )
        print("---------LOOPED----------") 
            
            

    
    
    
    def _update_axis(self):
        self.ax.clear()
        self.ax.set_xlim([0.1, DOMAIN])
        self.ax.set_ylim([0.1, DOMAIN])
        self.ax.set_xbound([0.1, DOMAIN])
        self.ax.set_ybound([0.1, DOMAIN])

    def startup(self):

        ani = FuncAnimation(self.fig, self.update, blit=False, interval=1)
        plt.show(block=True)
   
if __name__ == "__main__":
    time.sleep(0.5)
    display = Display()
    display.startup() 