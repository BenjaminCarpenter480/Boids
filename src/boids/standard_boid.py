import numpy as np
from parameters import Parameters as params
from typing import List
import logging
from base_boids import BaseBoid, BoidState

class StandardBoid(BaseBoid):
    """Standard boid follow behaviour class implementing basic flocking behaviours"""
    def __init__(self, boids: List['BaseBoid'], x: float, y: float, vx: float, vy: float) -> None:
        self._position = np.array([x, y], dtype=float)
        self._velocity = np.array([vx, vy], dtype=float)
        self._boids = boids
        self.logger = logging.getLogger("boids.boid")
        self.mass = 0.25


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
