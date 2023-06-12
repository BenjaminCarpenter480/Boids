import logging
import os
from random import randint, random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.linalg import norm

PIPE = "/tmp/boids"

DOMAIN = 1000
NUM_BOIDS = 20

turn_speed = 1
left_margin = 0.2*DOMAIN
right_margin = 0.8*DOMAIN
bottom_margin = 0.2*DOMAIN
top_margin = 0.8*DOMAIN

min_seperation = 0.05*DOMAIN
move_away_factor = 0.01

visual_dist = 0.1*DOMAIN
match_speed_factor = 0.1

centering_factor = 0

max_speed = 50
min_speed = 1

class Space():
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
        self.boid_list = []

        for i in range(NUM_BOIDS):
            self.boid_list.append(boid(self.boid_list,randint(1,DOMAIN), randint(1,DOMAIN), (random()), random(),randint(0,1)))
            time.sleep(0.1)



    def update(self, i, pipe_read):
        self._update_axis()
        
        for boid in pipe_read.readline.split(';'):
            b=boid.split(',')
            self.ax.quiver(float(b[0]),float(b[1]),float(b[2]),float(b[3]),
                           headlength=norm([float(b[2]),float(b[3])]) )            


    def _update_axis(self):
        self.ax.clear()
        self.ax.set_xlim([0.1, DOMAIN])
        self.ax.set_ylim([0.1, DOMAIN])
        self.ax.set_xbound([0.1, DOMAIN])
        self.ax.set_ybound([0.1, DOMAIN])

    def startup(self):
        try:
            try:
                os.remove(PIPE)
            except FileNotFoundError:
                pass
    
            os.mkfifo(PIPE)
            logging.info("Pipe created")
            self.pipe = open(PIPE, 'w')
            self.sim_loop()
        except FileExistsError as e:
            logging.error(f"Error in simulator: {e.strerror}")
        finally:
            try:
                os.remove(PIPE)
            except FileNotFoundError:
                pass
            logging.info("Pipe removed")
    
    
    def sim_loop(self):
        #Should probably keep open all loop so not read during write
        while True:
            for b in self.boid_list:

                b.move()
                b.write(self.pipe)
               
            self.pipe.write("\n")
            # time.sleep(1)
            print("loop")
            
class boid():
    def __init__(self,boids, x, y, vx, vy,bias=False) -> None:
        self._position = np.array([x,y],dtype=float)
        self._velocity = np.array([vx,vy],dtype=float)
        self._boids = boids
        self.bias = bias

    def write(self,pipe):
        pipe.write(f'{self.x},{self.y},{self.vx},{self.vy};')


    def move(self):
        #Move together
        """
        We work out the average velocity of "neighbouring" boids and then add the difference to the boids velocity with
        some small scaling factor  This acts to get them all moving the same direction
        """ 

        average_vel = np.array([0,0],dtype=float)
        average_pos = np.array([0,0],dtype=float)
        neighbours = 0
        for ob in self._boids:
            if(norm(ob.position - self.position) < visual_dist):
                average_vel += ob.velocity
                average_pos += ob.position
                neighbours += 1
                
        if(neighbours > 0):
            average_vel = average_vel/neighbours
            self.velocity += (average_vel-self.velocity)*match_speed_factor
            
            average_pos = average_pos/neighbours
            self.velocity += (average_pos-self.position)*centering_factor


        self.handle_edges()
        
        self.move_away()
        #if self.bias:
        #    self.velocity += np.random.rand(2)*max_speed

        speed =norm(self.velocity)
        if speed>max_speed:
            self.velocity = (self.velocity/speed)*max_speed
        elif speed<min_speed:
            self.velocity = (self.velocity/speed)*min_speed


        self.position += self.velocity

    def handle_edges(self):
        """
        When a boid reaches the edge of space (a wall) we want to modify its 
        velocity such that it will start to make a turn from the wall with every
        time step
        """
        if self.x < left_margin:
            self.vx = self.vx+turn_speed
        if self.x > right_margin:
            self.vx = self.vx-turn_speed
        if self.y < bottom_margin:
            self.vy = self.vy+turn_speed
        if self.y > top_margin:
            self.vy = self.vy-turn_speed


    def move_away(self):
        """
            Dealing with getting away from another boid that has gotten too 
            close, this is done by keeping creating a vecotr pointing in 
            opposite direction to any boids "too close" and then adding this to 
            some overall "move away" vector which is moved in (with some scaling)
        """
        move_away_vec = np.array([0,0],dtype=float)
        # move_away_x =0
        # move_away_y =0 
        for ob in self._boids:
            if(norm(ob.position - self.position) < min_seperation):
                move_away_vec += self.position - ob.position
                # move_away_x += self.x - ob.x
                # move_away_y += self.y - ob.y
        
        self.velocity += move_away_vec*move_away_factor                
        # self.vx += move_away_x*turn_speed
        # self.vy += move_away_y*turn_speed


    #Getters and Setters    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        assert value.any() < 1000
        self._position = value

    @property
    def velocity(self):
        
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        assert value.any()<1000
        self._velocity = value 

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, value):
        self._position[0] = value

    @property
    def y(self):
        return self._position[1]
    
    @y.setter
    def y(self, value):
        self._position[1] = value

    @property
    def vx(self):
        return self._velocity[0]
    
    @vx.setter
    def vx(self, value):
        self._velocity[0] = value

    @property
    def vy(self):
        return self._velocity[1]
    
    @vy.setter
    def vy(self, value):
        self._velocity[1] = value

if __name__ == "__main__":
    boids = Space()
    boids.startup()

