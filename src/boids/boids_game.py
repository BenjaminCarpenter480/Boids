import logging
import queue
from random import randint
import threading
import time

import numpy as np
import pygame
from parameters import Parameters
from pipe_boids import PipeReadHandler
BACKGROUND_COLOR = (255,255,255)

class BoidSprite():
    def __init__(self, x, y, vx, vy, world,parameter_file_path: str = 'parameters/default.yaml') -> None:
        self.kinematic_array  = np.array([0, 0, 0, 0])
        self.color = np.random.randint(0, 255, 3)
        self.parameters = Parameters(parameter_file_path)
        self.size = self.parameters.min_separation/20
        self.world = world

    def draw(self):
        pygame.draw.circle(self.world,
                           self.color,
                           self.convert_coords(self.kinematic_array[0], self.kinematic_array[1]),
                           self.size)

    @property
    def kinematic_vector(self):
        return self.kinematic_array

    @kinematic_vector.setter
    def kinematic_vector(self, np_array):
        self.kinematic_array = np_array
        self.draw()

    def convert_coords(self, x, y):
        x_t = (x/self.parameters.domain)*pygame.display.Info().current_w
        y_t = (y/self.parameters.domain)*pygame.display.Info().current_h
        return (x_t, y_t)


class GameVisuliser():
    boid_list = []
    def __init__(self,parameter_file_path: str = 'parameters/default.yaml') -> None:
        self.logger = logging.getLogger("boids.visualiser")
        self.parameters = Parameters(parameter_file_path)
        # Do not set level or add handlers here; handled by multiproc_logging
        pygame.init()

        print(pygame.display.get_desktop_sizes())
        win_size_x = pygame.display.get_desktop_sizes()[0][0]
        win_size_y = pygame.display.get_desktop_sizes()[0][1]
        if(self.parameters.domain < win_size_x or self.parameters.domain < win_size_y):
            win_size_x = self.parameters.domain
            win_size_y = self.parameters.domain
        else:
            win_size_x = int(win_size_x*0.8)
            win_size_y = int(win_size_y*0.8)

        self.world = pygame.display.set_mode((win_size_x, win_size_y))
        for _ in range(self.parameters.num_boids):
            self.boid_list.append(BoidSprite(randint(1,self.parameters.domain),
                                              randint(1,self.parameters.domain),
                                              0,
                                              0,
                                              self.world))

        self.pipe_access = PipeReadHandler(self.parameters.pipe)
        self.logger = logging.getLogger("boids.visualiser")
        # Do not set level or add handlers here; handled by multiproc_logging

    def update_boids(self):
        # while self.data.qsize() == 0:
        # TODO Convert to using ASYNC in place of threads and wait here?
        data = self.pipe_access.get_data()
        boids_from_pipe = data.split(';')

        self.logger.debug("Displaying %d boids", len(boids_from_pipe))
        for i in range(len(boids_from_pipe)-1):
            self.boid_list[i].kinematic_vector=np.array(boids_from_pipe[i].split(','),dtype=float)

    def update(self):
        self.update_boids()

        for event in pygame.event.get(): #Get all events in the queue
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def loop(self):
        while True:
            self.update()
            pygame.display.update() #Update the displaypane
            time.sleep(self.parameters.fps)
            self.world.fill(BACKGROUND_COLOR) #Clear the displaypane

if __name__== '__main__':
    game = GameVisuliser()
    game.loop()