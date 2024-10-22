import logging
import os
from random import randint, random
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from parameters import Parameters as params


class Space():
    def __init__(self) -> None:
        np.random.seed()
        self.fig, self.ax = plt.subplots()
        self.boid_list = []

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
        #Should probably keep open all loop so not read during write

        while True:
            for b in self.boid_list:
                b.move()

                b.write(self.pipe)
            self.pipe.write(bytes("\n",encoding='ASCII'))


class boid():
    def __init__(self,boids, x, y, vx, vy,bias=False) -> None:
        self.logger = logging.getLogger(__name__)
        self._position = np.array([x,y],dtype=float)
        self._velocity = np.array([vx,vy],dtype=float)
        self._boids = boids
        self.bias = NotImplemented
        self.mass = 0.25

    def write(self,pipe):
        pipe.write(bytes(f'{self.x},{self.y},{self.vx},{self.vy};', 'ASCII'))

    def move(self):
        """
        We work out the average velocity of "neighbouring" boids and then add the difference to the boids velocity with
        some small scaling factor  This acts to get them all moving the same direction
        """
        nearest_visual_neighbours, nearest_avoiding_neighbours, colliding_neighbours, local_average_pos, local_average_vel = self.nearest_neighbour_props()
        num_nearest_neighbours = len(nearest_visual_neighbours)
        self.logger.debug("Number of Nearest visual neighbours, avoiding neighbours, colliding neighbours: %s, %s, %s",
                          num_nearest_neighbours,len(nearest_avoiding_neighbours), len(colliding_neighbours))
        self.velocity = (self.velocity
                         +self.move_together(num_nearest_neighbours, local_average_pos, local_average_vel)
                         +self.handle_edges()
                         +self.move_away(nearest_avoiding_neighbours,colliding_neighbours)
                        )

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
        We work out the average velocity of "neighbouring" boids and then add the difference to the boids velocity with
        some small scaling factor  This acts to get them all moving the same direction
        """
        velocity_change = np.array([0,0],dtype=float)
        if(num_near_neighbours > 0):
            local_average_vel = local_average_vel/num_near_neighbours
            velocity_change += (local_average_vel-self.velocity)*params.match_speed_factor

            local_average_pos = local_average_pos/num_near_neighbours
            velocity_change += (local_average_pos-self.position)*params.centering_factor
        self.logger.debug("Velocity change due to moving together: %s", velocity_change)
        return velocity_change

    def move_away(self, nearest_avoiding_neighbours ,colliding_neighbours):
        """
            Dealing with getting away from another boid that has gotten too
            close, this is done by keeping creating a vector pointing in
            opposite direction to any boids "too close" and then adding this to
            some overall "move away" vector which is moved in (with some scaling)
        """
        diff_velocity_collide = np.array([0,0],dtype=float)
        for ob in colliding_neighbours:
            diff_velocity_collide  += ((self.mass-ob.mass)*self.velocity+2*ob.mass*ob.velocity)/(self.mass+ob.mass)

        self.logger.debug("Velocity change due to collisions away: %s", diff_velocity_collide)

        
        diff_velocity_avoid = np.array([0,0],dtype=float)

        for ob in nearest_avoiding_neighbours:
            diff_velocity_avoid += (self.position - ob.position)*params.move_away_factor

        self.logger.debug("Velocity change due to avoidance away: %s", diff_velocity_avoid)

        return diff_velocity_collide + diff_velocity_avoid

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

        self.logger.debug("Velocity change due to edge: %s", [diff_vx,diff_vy])
        return np.array([diff_vx,diff_vy],dtype=float)



    #Getters and Setters
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
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
    space = Space()
    space.run_loop()

