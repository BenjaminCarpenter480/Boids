import logging
import queue
from random import randint
import threading
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

        print(pygame.display.get_desktop_sizes())
        win_size_x = pygame.display.get_desktop_sizes()[0][0]
        win_size_y = pygame.display.get_desktop_sizes()[0][1]
        if(constants.DOMAIN < win_size_x or constants.DOMAIN < win_size_y):
            win_size_x = constants.DOMAIN
            win_size_y = constants.DOMAIN
        else:
            win_size_x = int(win_size_x*0.8)
            win_size_y = int(win_size_y*0.8)

        self.world = pygame.display.set_mode((win_size_x, win_size_y)) 
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
        self.pipe = open(boids_gen.PIPE, "rb")
        self.data = queue.Queue()
        self.pipe_reader = threading.Thread(target=self.empty_pipe)
        self.pipe_reader.start()


    def empty_pipe(self):
        # count = 0
        while self.pipe.readable():
            self.data.put(self.pipe.readline())
        

    def update_boids(self):
        # while self.data.qsize() == 0: #Convert to ASYNC?  
            
        
        data = self.data.get().decode('ASCII')
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
            time.sleep(1/60) # 30  fps
            self.world.fill(BACKGROUND_COLOR) #Clear the displaypane

if __name__== '__main__':
    game = Game_Space()
    game.loop()