"""
This module is responsible for visualising the boids on a plot using matplotlib
It reads the boid positions from a pipe given in the parameters and updates the
plot accordingly
"""
import logging
import os
import sys
from typing import Optional
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from parameters import Parameters as params
from pipe_boids import PipeReadHandler

class BoidVisualiser():
    """
    Visualiser class to display boids on a plot using matplotlib
    """
    def __init__(self) -> None:
        plt.close('all')
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, params.DOMAIN)
        self.ax.set_ylim(0, params.DOMAIN)
        self.ani: Optional[animation.FuncAnimation] = None

        # Calculate the marker size based on the min_separation
        # From https://stackoverflow.com/a/65177849
        marker_size = ((self.ax.transData.transform([params.min_separation/2,0])[0]
                                -self.ax.transData.transform([0,0])[0])**2*np.pi)


        self.boid_scatter = self.ax.scatter(np.zeros(params.NUM_BOIDS),
                                            np.zeros(params.NUM_BOIDS),
                                            s=marker_size,
                                            c=np.random.randint(0, 255, params.NUM_BOIDS))
        self.ax.tick_params(left = False, right = False , labelleft = False , 
                labelbottom = False, bottom = False)
        self.pipe_access = PipeReadHandler(params.PIPE)
        self.logger = logging.getLogger("boids.visualiser")


    def update_boids(self, _):
        """
        Update boid positions on plot
        """
        data = self.pipe_access.get_data()
        if not data or not data.strip():
            return self.boid_scatter,
        boids_from_pipe = data.split(';')
        self.logger.debug("Displaying %d boids", len(boids_from_pipe))
        boid_positions = []
        for boid_str in boids_from_pipe[:-1]:
            x, y, _, _ = map(float, boid_str.split(','))
            boid_positions.append([x, y])

        self.boid_scatter.set_offsets(boid_positions)
        return self.boid_scatter,

    def animate(self, save_video: str | None = None, frames: int = 1000, fps: int = 30):
        """
        Main entry point to startup the visualiser loop or save as a video
        """
        self.logger.info("Starting animation")
        self.logger.info(f"Save video value: {save_video}")
        self.ani = animation.FuncAnimation(self.fig,
                                       self.update_boids,
                                       blit=True,
                                       interval=5 if not save_video else 1000 // fps,
                                       frames=frames
                                       )
        if save_video:
            self.logger.info("Saving animation to %s", save_video)
            writer = animation.FFMpegWriter(fps=fps)
            self.ani.save(save_video, writer=writer)
            self.logger.info("Saved animation to %s", save_video)
            os._exit(0)
        else:
            plt.show()
            sys.exit()

    def save_video(self, filename: str = "boids_animation.mp4", frames: int = 1000, fps: int = 30):
        """
        Save the animation to a video file
        """
        matplotlib.use('Agg')
        self.animate(save_video=filename, frames=frames, fps=fps)


if __name__ == '__main__':
    visualiser = BoidVisualiser()
    visualiser.animate()
