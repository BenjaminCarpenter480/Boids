class Parameters:
    FPS = 1/60
    PIPE = "/tmp/boids_pipe"
    DOMAIN = 8000
    NUM_BOIDS = 50
    STEP_SIZE=1

    turn_speed = 1
    left_margin = 0
    right_margin = DOMAIN
    bottom_margin = DOMAIN
    top_margin = 0

    # Size of a boid, if they get within 2* this distance to another boid they are considered collided
    
    move_away_factor = 0.5

    visual_dist    = 500 # Distance a boid can see, they'll try to match speed and move towards the average position of boids in this range
    avoid_dist     = 400 # Distance at which boids will act to move apart
    min_seperation = 50  # Size of a boid, if they get within 2* this distance to another boid they are considered collided
    
    match_speed_factor = 1
    centering_factor = 0

    max_speed = 25
    min_speed = 1
