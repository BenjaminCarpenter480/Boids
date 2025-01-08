# Boids Simulation

This is a personal "fun" project to simulate and visualize the behavior of boids using Python. Boids are a type of artificial life program, simulating the flocking behavior of birds. The simulation mimics the way birds fly in flocks, fish swim in schools, or herds of animals move together.

![boids_animation](https://github.com/user-attachments/assets/8741bfe7-2242-4939-8741-8c6b206691d1)


## What are Boids?

Boids are a type of artificial life program, developed by Craig Reynolds in 1986, which simulates the flocking behavior of birds. The name "boid" corresponds to a shortened version of "bird-oid object", which refers to a bird-like object. Boids are governed by three simple rules:
1. **Separation**: Avoid crowding neighbors (short-range repulsion).
2. **Alignment**: Steer towards the average heading of neighbors.
3. **Cohesion**: Steer towards the average position of neighbors (long-range attraction).

These simple rules result in complex and realistic flocking behavior.

## Project Description

This project simulates the behavior of boids using Python and visualizes the simulation using either Pygame (older testing around) or Matplotlib (recommended). The project is not intended to be a novel or optimal solution (would have used C++ if I wanted many many boids on the screen at once). It is a personal project for fun and learning as I was inspired by the murmuration behaviours seen in this video.
[![Coding Adventures:Boids](https://img.youtube.com/vi/bqtqltqcQhw/0.jpg)](https://youtu.be/bqtqltqcQhw?si=R_I6dIl4QQxESqK9)


## Running the Simulation

To run the simulation and view the animation, follow these steps:

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd Boids
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the simulation with Matplotlib:
    ```sh
    python src/boids/boids_runner.py matplotlib
    ```
