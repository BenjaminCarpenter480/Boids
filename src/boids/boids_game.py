import logging
import queue
from random import randint
import threading
import time

import numpy as np
import pygame
from parameters import Parameters as params
BACKGROUND_COLOR = (255,255,255)

class PipeReadHandler():
    """
    For reading data from the generator object

    Data is returned as a string with each boid seperated by a ';' and each "," seperating the boid
    attributes in the form x,y,vx,vy
    """

    def __init__(self, pipe_address=params.PIPE) -> None:
        """Class to handle reading from the pipe
        """
        self.__pipe = open(pipe_address,"rb")
        self.__data = queue.Queue()
        self.__pipe_reader = threading.Thread(target=self.empty_pipe)
        self.__pipe_reader.start()

    def empty_pipe(self):
        """
        Read from the pipe and put the data in the queue to be accessed by the process
        """
        while self.__pipe.readable():
            self.__data.put(self.__pipe.readline())

    def get_data(self):
        """Data stored in the pipe
        """
        return self.__data.get().decode('ASCII')

class BoidSprite():
    def __init__(self, x, y, vx, vy, world) -> None:
        self.kinematic_array  = np.array([0, 0, 0, 0])
        self.color = np.random.randint(0, 255, 3)
        self.size = params.min_seperation/20
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
        x_t = (x/params.DOMAIN)*pygame.display.Info().current_w
        y_t = (y/params.DOMAIN)*pygame.display.Info().current_h
        return (x_t, y_t)




class GameVisuliser():
    boid_list = []
    def __init__(self) -> None:
        pygame.init()

        print(pygame.display.get_desktop_sizes())
        win_size_x = pygame.display.get_desktop_sizes()[0][0]
        win_size_y = pygame.display.get_desktop_sizes()[0][1]
        if(params.DOMAIN < win_size_x or params.DOMAIN < win_size_y):
            win_size_x = params.DOMAIN
            win_size_y = params.DOMAIN
        else:
            win_size_x = int(win_size_x*0.8)
            win_size_y = int(win_size_y*0.8)

        self.world = pygame.display.set_mode((win_size_x, win_size_y))
        for _ in range(params.NUM_BOIDS):
            self.boid_list.append(BoidSprite(randint(1,params.DOMAIN),
                                              randint(1,params.DOMAIN),
                                              0,
                                              0,
                                              self.world))

        self.pipe_access = PipeReadHandler(params.PIPE)
        self.logger = logging.getLogger(__name__)

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
            time.sleep(params.FPS)
            self.world.fill(BACKGROUND_COLOR) #Clear the displaypane

if __name__== '__main__':
    game = GameVisuliser()
    game.loop()