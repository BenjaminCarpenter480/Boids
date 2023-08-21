from boids_gen import boid
class bboid(boid):
    def __init__(self, boids, x, y, vx, vy, bias=False) -> None:
        super().__init__(boids, x, y, vx, vy, bias)
        
    