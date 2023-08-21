from random import randint, random
import time
import pygame
import boids_gen
from boids_gen import boid
import constants #TODO Rename to something more specific

BACKGROUND_COLOR = (255,255,255)

class boid_sprite(boid):
    def __init__(self, boids, x, y, vx, vy, world) -> None:
        super().__init__(boids, x, y, vx, vy)
        self.color = (0,0,0)
        self.size = 5
        self.world = world
        
    def draw(self):
        pygame.draw.circle(self.world,
                           self.color,
                           self.convert_coords(self.x, self.y),
                           self.size)
    
    def update(self):
        self.move()
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
            self.boid_list.append(boid_sprite(self.boid_list,
                                              randint(1,constants.DOMAIN),
                                              randint(1,constants.DOMAIN),
                                              0,
                                              0,
                                              self.world))



    def update(self):
        for boid in self.boid_list:
            boid.update()
        for event in pygame.event.get(): #Get all events in the queue
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    def loop(self):
        while True:
            self.update()
            pygame.display.update() #Update the displaypane
            time.sleep(0.1)
            self.world.fill(BACKGROUND_COLOR) #Clear the displaypane

if __name__== '__main__':
    game = Game_Space()
    game.loop()