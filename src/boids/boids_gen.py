"""
This file defines the boid class which define each boids kinematics and space class which defines 
the time and space the boids move in.
"""
import logging
import os
from random import randint, random
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from parameters import Parameters as params


class Space():
    def __init__(self) -> None:
        """
        Class to define the space in which boids move, includes the boids update loop
        """
        np.random.seed()
        self.fig, self.ax = plt.subplots()
        self.boid_list = []
        self.pipe = None

        try:
            os.remove(params.PIPE)
        except FileNotFoundError:
            pass
        try:
            os.mkfifo(params.PIPE)
            logging.info("Pipe created")
        except FileNotFoundError as e:
            logging.error("Error creating pipe: %s", e.strerror)
            raise e

        for _ in range(params.NUM_BOIDS):
            self.boid_list.append(boid(self.boid_list,randint(1,params.DOMAIN),
                                        randint(1,params.DOMAIN),
                                        (random()),
                                        random(),
                                        randint(0,1)))

    def run_loop(self):
        """
        Startup loop to generate simulation data related to boid positions which
        is written to a pipe defined in the parameters file

        Includes handling of the pipe creation and deletion
        """
        try:
            self.pipe = open(params.PIPE, 'wb')
            logging.info("Pipe loaded on write side")
            self.sim_loop()
        except FileExistsError as e:
            logging.error("Error in simulator: %s", e.strerror)
            self.pipe.close()
        finally:
            try:
                os.remove(params.PIPE)
            except FileNotFoundError:
                pass
            logging.info("Pipe removed")


    def sim_loop(self):
        """
        Simulation loop to move boids and write their positions to the pipe
        """
        while True:
            for b in self.boid_list:
                b.move()

                b.write(self.pipe)
            self.pipe.write(bytes("\n",encoding='ASCII'))

class boid():
    def __init__(self,boids, x, y, vx, vy, bias=False) -> None:
        """
        Class defining a boid object with a position and velocity

        Args:
            x (float): x position
            y (float): y position
            vx (float): x velocity
            vy (float): y velocity
            bias: Not implemented feature
        """
        self._position = np.array([x,y],dtype=float)
        self._velocity = np.array([vx,vy],dtype=float)
        self._boids = boids
        self.bias = NotImplemented

    def write(self,pipe):
        """
        Write the boid position and velocity to the pipe
        """
        pipe.write(bytes(f'{self.x},{self.y},{self.vx},{self.vy};', 'ASCII'))

    def move(self):
        """
        We work out the average velocity of "neighbouring" boids and then add the difference to the 
        boids velocity with some small scaling factor  This acts to get them all moving the same
        direction
        """

        nearest_neighbours, colliding_neighbours, local_average_pos, local_average_vel\
                                                                 = self.nearest_neighbour_props()
        num_nearest_neighbours = len(nearest_neighbours)
        self.velocity = (self.velocity
                    +self.move_together(num_nearest_neighbours,local_average_pos,local_average_vel)
                    +self.handle_edges()
                    +self.move_away()
                        )

        self.limit_speed()

        self.position += self.velocity*params.STEP_SIZE

    def move_together(self, num_near_neighbours, local_average_pos, local_average_vel):
        """
        We work out the average velocity of "neighbouring" boids and then add the difference to the
        boids velocity with some small scaling factor  
        This acts to get them all moving the same direction
        """
        velocity_change = np.array([0,0],dtype=float)
        if num_near_neighbours > 0:
            local_average_vel = local_average_vel/num_near_neighbours
            velocity_change += (local_average_vel-self.velocity)*params.match_speed_factor

            local_average_pos = local_average_pos/num_near_neighbours
            velocity_change += (local_average_pos-self.position)*params.centering_factor

        return velocity_change

    def nearest_neighbour_props(self):
        """
        Find the nearest neighbours to the boid and return the list of these, the average position
        and velocity of these neighbours
        """
        local_average_vel = np.array([0,0],dtype=float)
        local_average_pos = np.array([0,0],dtype=float)
        nearest_neighbours:set = set()
        colliding_neighbours:set = set()
        for ob in self._boids:
            if(calc_norm := norm(ob.position - self.position) < params.visual_dist):
                local_average_vel += ob.velocity
                local_average_pos += ob.position
                nearest_neighbours.add(ob)
                if calc_norm < 2*params.min_seperation:
                    colliding_neighbours.add(ob)


        return nearest_neighbours, colliding_neighbours, local_average_pos,local_average_vel

    def limit_speed(self):
        """
        Prevent boids from moving too fast or too slow, simply by normalising the velocity vector
        for correct direction and then multiplying by the max or min speed if the speed is too high
        or low

        Needs to really use the current speef of the boid not the previous step speed.
        """
        speed =norm(self.velocity)
        if speed>params.max_speed:
            self.velocity = (self.velocity/speed)*params.max_speed
        elif speed<params.min_speed:
            self.velocity = (self.velocity/speed)*params.min_speed

    def handle_edges(self):
        """
        When a boid reaches the edge of space (a wall) we want to modify its
        velocity such that it will start to make a turn from the wall with every
        time step
        """
        diff_vx = 0
        diff_vy = 0
        #TODO: We want turn speed to be a function of the distance from the wall, increasing the
        # closer we are to the wall (so the boid doesn't hit the wall!)
        if self.x < params.left_margin:
            diff_vx = params.turn_speed
        if self.x > params.right_margin:
            diff_vx = -params.turn_speed
        if self.y < params.bottom_margin:
            diff_vy = params.turn_speed
        if self.y > params.top_margin:
            diff_vy  = -params.turn_speed

        return np.array([diff_vx,diff_vy],dtype=float)

    def move_away(self):
        """
            Dealing with getting away from another boid that has gotten too
            close, this is done by keeping creating a vector pointing in
            opposite direction to any boids "too close" and then adding this to
            some overall "move away" vector which is moved in (with some scaling)
        """
        move_away_vec = np.array([0,0],dtype=float)
        for ob in self._boids:
            if norm(ob.position - self.position) < params.min_seperation:
                move_away_vec += self.position - ob.position

        return move_away_vec*params.move_away_factor


    #Getters and Setters
    @property
    def position(self):#pylint: disable=missing-function-docstring # self documenting
        return self._position

    @position.setter
    def position(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._position = value

    @property
    def velocity(self):#pylint: disable=missing-function-docstring # self documenting
        return self._velocity

    @velocity.setter
    def velocity(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._velocity = value

    @property
    def x(self):#pylint: disable=missing-function-docstring # self documenting
        return self._position[0]

    @x.setter
    def x(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._position[0] = value

    @property
    def y(self):#pylint: disable=missing-function-docstring # self documenting
        return self._position[1]

    @y.setter
    def y(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._position[1] = value

    @property
    def vx(self):#pylint: disable=missing-function-docstring # self documenting
        return self._velocity[0]

    @vx.setter
    def vx(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._velocity[0] = value

    @property
    def vy(self):#pylint: disable=missing-function-docstring # self documenting
        return self._velocity[1]

    @vy.setter
    def vy(self, value):#pylint: disable=missing-function-docstring # self documenting
        self._velocity[1] = value

if __name__ == "__main__":
    space = Space()
    space.run_loop()
