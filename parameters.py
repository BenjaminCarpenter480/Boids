class Parameters:
    FPS = 1/60
    PIPE = "/tmp/boids"
    DOMAIN = 5000
    NUM_BOIDS = 40
    STEP_SIZE=1

    turn_speed = 1
    left_margin = 0.2*DOMAIN
    right_margin = 0.8*DOMAIN
    bottom_margin = 0.2*DOMAIN
    top_margin = 0.8*DOMAIN

    min_seperation = 0.05*DOMAIN
    move_away_factor = 0.01

    visual_dist = 0.1*DOMAIN
    match_speed_factor = 0.1

    centering_factor = 0.001

    max_speed = 25
    min_speed = 1