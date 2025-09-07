"""
This file defines the boid class which define each boids kinematics and space class which defines 
the time and space the boids move in.
"""
import logging
import os
from random import randint, random
from typing import List
import numpy as np
from numpy.linalg import norm
from parameters import Parameters as params


class Space:
    def __init__(self) -> None:
        """Initialize the space containing boids"""
        np.random.seed()
        self.boid_list: List[Boid] = []
        self.pipe = None
        self._setup_pipe()
        self._initialize_boids()

    def _setup_pipe(self) -> None:
        """Setup the communication pipe"""
        try:
            os.remove(params.PIPE)
        except FileNotFoundError:
            pass
        
        try:
            os.mkfifo(params.PIPE)
            logging.info("Pipe created")
        except OSError as e:
            logging.error("Error creating pipe: %s", str(e))
            raise

    def _initialize_boids(self) -> None:
        """Initialize boid population"""
        # First, create boids with a temporary empty list
        self.boid_list = [
            Boid(
                [],
                randint(1, params.DOMAIN),
                randint(1, params.DOMAIN),
                random(),
                random()
            ) for _ in range(params.NUM_BOIDS)
        ]
        # Now update each boid's _boids reference to the full list
        for boid in self.boid_list:
            boid._boids = self.boid_list

    def __del__(self) -> None:
        """Cleanup resources"""
        if self.pipe:
            self.pipe.close()
        try:
            os.remove(params.PIPE)
        except FileNotFoundError:
            pass

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

class Boid:
    def __init__(self, boids: List['Boid'], x: float, y: float, 
                 vx: float, vy: float) -> None:
        """
        Initialize a boid with position and velocity
        
        Args:
            boids: List of all boids in the simulation
            x, y: Initial position
            vx, vy: Initial velocity
        """
        self._position = np.array([x, y], dtype=float)
        self._velocity = np.array([vx, vy], dtype=float)
        self._boids = boids
        self.mass = 0.25

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
        nearest_visual_neighbours, nearest_avoiding_neighbours, colliding_neighbours, local_average_pos, local_average_vel = self.nearest_neighbour_props()
        num_nearest_neighbours = len(nearest_visual_neighbours)
        self.logger.debug("Number of Nearest visual neighbours, avoiding neighbours, colliding neighbours: %s, %s, %s",
                          num_nearest_neighbours,len(nearest_avoiding_neighbours), len(colliding_neighbours))
        self.velocity = (self.velocity
                         +self.move_together(num_nearest_neighbours, local_average_pos, local_average_vel)
                         +self.move_away(nearest_avoiding_neighbours)
                        )

        self.handle_interboid_collisions(colliding_neighbours)
        self.handle_edges()
        self.limit_speed()

        self.position += self.velocity*params.STEP_SIZE

    def nearest_neighbour_props(self):
        local_average_vel = np.array([0,0],dtype=float)
        local_average_pos = np.array([0,0],dtype=float)
        nearest_visual_neighbours:set = set()
        colliding_neighbours:set = set()
        avoiding_neighbours:set = set()
        for ob in self._boids:
            if((calc_norm := norm(ob.position - self.position)) < params.visual_dist):
                local_average_vel += ob.velocity
                local_average_pos += ob.position
                self.logger.debug("Norm between boids: %s", calc_norm)
                if(calc_norm < 2*params.min_seperation):
                    colliding_neighbours.add(ob)
                elif(calc_norm < params.avoid_dist):
                    avoiding_neighbours.add(ob)
                else:
                    nearest_visual_neighbours.add(ob)
        
        self.logger.debug("Nearest visual neighbours position and velocity: %s, %s",
                           local_average_vel, local_average_vel)


        return (nearest_visual_neighbours, avoiding_neighbours, colliding_neighbours,
                local_average_pos,local_average_vel)


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
        self.logger.debug("Velocity change due to moving together: %s", velocity_change)
        return velocity_change

    def move_away(self, nearest_avoiding_neighbours):
        """
            Dealing with getting away from another boid that has gotten too
            close, this is done by keeping creating a vector pointing in
            opposite direction to any boids "too close" and then adding this to
            some overall "move away" vector which is moved in (with some scaling)

            We also handle collisions with the 'wall' here, by considering the wall as a form of 
            elastic collision
        """ 
        diff_velocity_avoid = np.array([0,0],dtype=float)

        for ob in nearest_avoiding_neighbours:
            diff_velocity_avoid += (self.position - ob.position)*params.move_away_factor

        self.logger.debug("Velocity change due to avoidance away: %s", diff_velocity_avoid)

        return  diff_velocity_avoid

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

    def handle_interboid_collisions(self, colliding_neighbours):
        for ob in colliding_neighbours:
            self.velocity = ((self.mass-ob.mass)*self.velocity+2*ob.mass*ob.velocity)/(self.mass+ob.mass)


    def handle_edges(self):
        """
        When a boid reaches the edge of space (a wall) we want to modify its
        velocity such that it will start to make a turn from the wall with every
        time step
        """
        if self.x < params.left_margin:
            self.velocity[0] =  abs(self.velocity[0])
        if self.x > params.right_margin:
            self.velocity[0] = -abs(self.velocity[0])
        if self.y > params.bottom_margin:
            self.velocity[1] = -abs(self.velocity[1])
        if self.y < params.top_margin:
            self.velocity[1] = abs(self.velocity[1])

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
