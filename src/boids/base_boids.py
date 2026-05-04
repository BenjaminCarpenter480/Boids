from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from parameters import Parameters as params
from numpy.linalg import norm
from typing import List
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
    """Base class for all boid implementations
    
    This will basically decide the overall structure of the class and physical interactions between 
    boids such as collisions and edge conditions. 
    
    """
    def __init__(self, boids: List['BaseBoid'], x: float, y: float, vx: float, vy: float) -> None:
        self._position = np.array([x, y], dtype=float)
        self._velocity = np.array([vx, vy], dtype=float)
        self._boids = boids
        self.logger = logging.getLogger("boids.boid")
        self.mass = 0.25

    def move(self):
        """Overall movement logic for a boid called at each time step
        
        """


        nearest_visual_neighbours, nearest_avoiding_neighbours, colliding_neighbours,\
            local_average_pos, local_average_vel = self.nearest_neighbour_props()
        num_nearest_neighbours = len(nearest_visual_neighbours)

        # Handle flocking/ 'decided' movement first
        self.velocity = (self.velocity
                    +self.move_random()
                    +self.move_together(num_nearest_neighbours,local_average_pos,local_average_vel)
                    +self.move_away(nearest_avoiding_neighbours)
                        )

        self.position += self.velocity*params.STEP_SIZE

        self.handle_edges()

        self.logger.debug(
            "Boid at (%.2f, %.2f) with velocity (%.2f, %.2f) has %d neighbours and %d colliding",
            self.x, self.y, self.vx, self.vy,
            num_nearest_neighbours, len(colliding_neighbours)
        )

    def move_random(self):
        """
        Add a small random velocity change to the boid to prevent it getting stuck
        in a local minima
        """
        move_randomly:bool = np.random.random() < params.MOVE_RANDOM_PROBABILITY
        if move_randomly:
            random_velocity = (np.random.rand(2)-0.5)*2*params.randomness_factor
            self.logger.debug("Random velocity change: %s", random_velocity)
            return random_velocity
        return np.array([0,0],dtype=float)

    def move_together(self, num_near_neighbours, local_average_pos, local_average_vel):
        """
        In this base implementation, we do not implement any specific behavior for moving together;
        this method can be overridden in subclasses to define specific flocking behavior.
        """
        velocity_change = np.array([0,0],dtype=float)
        self.logger.debug("Velocity change due to moving together: %s", velocity_change)
        return velocity_change

    def move_away(self, nearest_avoiding_neighbours):
        """
        In this base implementation, we do not implement any specific behavior for moving away;
        this method can be overridden in subclasses to define specific avoidance behavior.
        """
        diff_velocity_avoid = np.array([0,0],dtype=float)

        self.logger.debug("Velocity change due to avoidance away: %s", diff_velocity_avoid)

        return  diff_velocity_avoid

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
                if calc_norm < 2*params.min_separation:
                    colliding_neighbours.add(ob)
                elif calc_norm < params.avoid_dist:
                    avoiding_neighbours.add(ob)
                else:
                    nearest_visual_neighbours.add(ob)

        self.logger.debug("Nearest visual neighbours position and velocity: %s, %s",
                           local_average_pos, local_average_vel)


        return (nearest_visual_neighbours, avoiding_neighbours, colliding_neighbours,
                local_average_pos,local_average_vel)

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
                    
                self.handle_interboid_collisions()
                    
                for boid in self.boid_list:
                    self.comm.write_state(boid.state)

                self.comm.write_frame_end()
        finally:
            self.comm.cleanup()


    def handle_interboid_collisions(self):
        """
        Handle collisions between boids across the whole space.
        """
        for i, bi in enumerate(self.boid_list):
            for j, bj in enumerate(self.boid_list):
                if i < j:
                    self._resolve_pair_collision(bi, bj)  

    def _resolve_pair_collision(self, b1, b2) -> None:
        """Apply elastic impulse between two boids if they overlap"""
        delta_pos = b1.position - b2.position
        dist = norm(delta_pos)
        
        # Check if overlapping (adjust threshold as needed)
        if dist < 2 * params.min_separation:
            n = delta_pos / dist  # unit normal from b2 -> b1
            v_rel = b1.velocity - b2.velocity
            v_rel_n = np.dot(v_rel, n)
            
            # Only collide if approaching
            if v_rel_n < 0:
                j = -v_rel_n / (1/b1.mass + 1/b2.mass)  # e=1 for elastic
                b1.velocity += (j / b1.mass) * n
                b2.velocity -= (j / b2.mass) * n