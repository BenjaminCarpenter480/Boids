from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from parameters import Parameters as params
from numpy.linalg import norm
from typing import List, Optional
import logging

@dataclass
class BoidState:
    """Data structure for boid state"""
    x: float
    y: float
    vx: float
    vy: float

class CommunicationStrategy(ABC):
    """Protocol for different communication methods"""
    def write_state(self, state: BoidState) -> None: ...
    def write_frame_end(self) -> None: ...
    def cleanup(self) -> None: ...

class BaseBoid(ABC):
    """Base class for all boid implementations"""
    def __init__(self, boids: List['BaseBoid'], x: float, y: float, vx: float, vy: float) -> None:
        self._position = np.array([x, y], dtype=float)
        self._velocity = np.array([vx, vy], dtype=float)
        self._boids = boids
        self.logger = logging.getLogger("boids.boid")
        self.mass = 0.25


    def move(self):
        """
        We work out the average velocity of "neighbouring" boids and then add the difference to the
        boids velocity with some small scaling factor  This acts to get them all moving the same
        direction
        """

        nearest_visual_neighbours, nearest_avoiding_neighbours, colliding_neighbours, local_average_pos, local_average_vel = self.nearest_neighbour_props()
        num_nearest_neighbours = len(nearest_visual_neighbours)
        self.velocity = (self.velocity
                    +self.move_together(num_nearest_neighbours,local_average_pos,local_average_vel)
                    +self.move_away(nearest_avoiding_neighbours)
                        )

        self.handle_interboid_collisions(colliding_neighbours)
        self.handle_edges()
        self.limit_speed()

        self.position += self.velocity*params.STEP_SIZE

        self.logger.debug(
            "Boid at (%.2f, %.2f) with velocity (%.2f, %.2f) has %d neighbours and %d colliding",
            self.x, self.y, self.vx, self.vy,
            num_nearest_neighbours, len(colliding_neighbours)
        )

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


    def nearest_neighbour_props(self):
        """
        Find the nearest neighbours to the boid and return the list of these, the average position
        and velocity of these neighbours
        We also return a list of boids that are too close (colliding) and those that are in the
        avoid distance
        """
        local_average_vel = np.array([3,0],dtype=float)
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

    def handle_interboid_collisions(self, colliding_neighbours):
        for ob in colliding_neighbours:
            self.velocity = ((self.mass-ob.mass)*self.velocity+2*ob.mass*ob.velocity)/(self.mass+ob.mass)


    def limit_speed(self):
        """
        Prevent boids from moving too fast or too slow, simply by normalising the velocity vector
        for correct direction and then multiplying by the max or min speed if the speed is too high
        or low

        Needs to really use the current speed of the boid not the previous step speed.
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
        if self.x < params.left_margin:
            self.velocity[0] =  abs(self.velocity[0])
        if self.x > params.right_margin:
            self.velocity[0] = -abs(self.velocity[0])
        if self.y > params.bottom_margin:
            self.velocity[1] = -abs(self.velocity[1])
        if self.y < params.top_margin:
            self.velocity[1] = abs(self.velocity[1])

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


    @property
    def state(self) -> BoidState:
        """Get current boid state"""
        return BoidState(self.x, self.y, self.vx, self.vy)

class BaseSpace(ABC):
    """Base class for all space implementations"""
    def __init__(self, comm_strategy: CommunicationStrategy) -> None:
        self.logger = logging.getLogger("boids.space")
        # Do not set level or add handlers here; handled by multiproc_logging
        self.boid_list: List[BaseBoid] = []
        self.comm = comm_strategy
        self._initialize_boids()

    @abstractmethod
    def _initialize_boids(self) -> None:
        """Initialize boid population"""

    def sim_loop(self) -> None:
        """Core simulation loop"""
        try:
            while True:
                for boid in self.boid_list:
                    boid.move()
                    self.comm.write_state(boid.state)
                self.comm.write_frame_end()
        finally:
            self.comm.cleanup()
