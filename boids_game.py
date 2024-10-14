import logging
import queue
from random import randint, random
import time

import numpy as np
import pygame
import boids_gen
from boids_gen import boid
import constants #TODO Rename to something more specific

BACKGROUND_COLOR = (255,255,255)

class boid_sprite(boid):
    def __init__(self, x, y, vx, vy, world) -> None:
        # super().__init__(boids, x, y, vx, vy)
        self.kinematic_array  = np.array([0, 0, 0, 0]) #TODO: Change to start value 
        self.color = (0,0,0)
        self.size = 5
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
        x_t = (x/constants.DOMAIN)*pygame.display.Info().current_w
        y_t = (y/constants.DOMAIN)*pygame.display.Info().current_h
        return (x_t, y_t)


class Game_Space():
    boid_list = []
    def __init__(self) -> None:
        pygame.init()
        self.world = pygame.display.set_mode((constants.DOMAIN, constants.DOMAIN))
        for i in range(constants.NUM_BOIDS):
            self.boid_list.append(boid_sprite(randint(1,constants.DOMAIN),
                                              randint(1,constants.DOMAIN),
                                              0,
                                              0,
                                              self.world))
        self.pipe_init()
        self.logger = logging.getLogger(__name__)

    # pipe handling and update code

    def pipe_init(self):
            self.pipe = open(boids_gen.PIPE, "r")
            self.data = queue.Queue()


    def empty_pipe(self):
        count = 0
        while self.pipe.readable() and count < 500:
            self.data.put(self.pipe.readline())
            count = count +1

    def update_boids(self):
        while self.data.qsize() == 0:
            self.empty_pipe()
        
        data = self.data.get()
        boids_from_pipe = data.split(';')
        
        self.logger.debug("Displaying %d boids", len(boids_from_pipe))
        for i in range(len(boids_from_pipe)-1):
            self.boid_list[i].kinematic_vector=np.array(boids_from_pipe[i].split(','),dtype=float)
            # self.boid_list[i].draw()


    def update(self):
        #Do something!
        self.update_boids()

        #Then
        for event in pygame.event.get(): #Get all events in the queue
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    def loop(self):
        while True:
            self.update()
            pygame.display.update() #Update the displaypane
            time.sleep(0.01)
            self.world.fill(BACKGROUND_COLOR) #Clear the displaypane

if __name__== '__main__':
    game = Game_Space()
    game.loop()