import logging
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from parameters import Parameters as params
from boids_game import PipeReadHandler

class BoidVisualiser():
    def __init__(self) -> None:
        plt.close('all')
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, params.DOMAIN)
        self.ax.set_ylim(0, params.DOMAIN)

        # Calculate the marker size based on the min_seperation
        # From https://stackoverflow.com/a/65177849
        marker_size = (2*(self.ax.transData.transform([params.min_seperation,0])[0]
                                -self.ax.transData.transform([0,0])[0]))**2
        
        
        self.boid_scatter = self.ax.scatter(np.zeros(params.NUM_BOIDS),
                                            np.zeros(params.NUM_BOIDS),
                                            s=marker_size,
                                            c=np.random.randint(0, 255, params.NUM_BOIDS))
        self.ax.set_xlim(-params.DOMAIN*0.2, params.DOMAIN*1.2)
        self.ax.set_ylim(-params.DOMAIN*0.2, params.DOMAIN*1.2)
        self.ax.scatter(0,0)
        self.ax.scatter(0,params.DOMAIN)
        self.ax.scatter(params.DOMAIN, params.DOMAIN)
        self.ax.scatter(params.DOMAIN, 0)
        self.ax.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False)
        self.pipe_access = PipeReadHandler(params.PIPE)
        self.logger = logging.getLogger(__name__)


    def update_boids(self, _):
        data = self.pipe_access.get_data()
        boids_from_pipe = data.split(';')
        self.logger.debug("Displaying %d boids", len(boids_from_pipe))
        boid_positions = []
        for boid_str in boids_from_pipe[:-1]:
            x, y, vx, vy = map(float, boid_str.split(','))
            boid_positions.append([x, y])

        self.boid_scatter.set_offsets(boid_positions)
        return self.boid_scatter,

    def animate(self):
        self.logger.info("Starting animation")
        self.ani = animation.FuncAnimation(self.fig,
                                       self.update_boids,
                                       blit=True,
                                       interval=5,
                                       frames=1000
                                       )
        plt.show()
        sys.exit()


if __name__ == '__main__':
    visualiser = BoidVisualiser()
    visualiser.animate()