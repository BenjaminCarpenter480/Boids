"""
This module is responsible for visualising the boids on a plot using matplotlib
It reads the boid positions from a pipe given in the parameters and updates the
plot accordingly
"""
import logging
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from parameters import Parameters as params
from boids_game import PipeReadHandler

class BoidVisualiser():
    """
    Visualiser class to display boids on a plot using matplotlib
    """
    def __init__(self) -> None:
        plt.close('all')
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, params.DOMAIN)
        self.ax.set_ylim(0, params.DOMAIN)
        self.ani = None
        # Calculate the marker size based on the min_seperation
        # From https://stackoverflow.com/a/65177849
        marker_size = (2*(self.ax.transData.transform([params.min_seperation,0])[0]
                                -self.ax.transData.transform([0,0])[0]))


        self.boid_scatter = self.ax.scatter(np.zeros(params.NUM_BOIDS),
                                            np.zeros(params.NUM_BOIDS),
                                            s=marker_size,
                                            c=np.random.randint(0, 255, params.NUM_BOIDS))
        self.ax.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
        self.pipe_access = PipeReadHandler(params.PIPE)
        self.logger = logging.getLogger(__name__)


    def update_boids(self, _):
        """
        Update boid positions on plot
        """
        data = self.pipe_access.get_data()
        boids_from_pipe = data.split(';')
        self.logger.debug("Displaying %d boids", len(boids_from_pipe))
        boid_positions = []
        for boid_str in boids_from_pipe[:-1]:
            x, y, _, _ = map(float, boid_str.split(','))
            boid_positions.append([x, y])

        self.boid_scatter.set_offsets(boid_positions)
        return self.boid_scatter,

    def animate(self):
        """
        Main entry point to startup the visualiser loop
        """
        self.logger.info("Starting animation")
        self.ani = animation.FuncAnimation(self.fig,
                                       self.update_boids,
                                       blit=True,
                                       interval=5,
                                       frames=1000
                                       )
        plt.show()


if __name__ == '__main__':
    visualiser = BoidVisualiser()
    visualiser.animate()
