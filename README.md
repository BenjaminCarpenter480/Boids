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

## Architecture Overview

The project follows a modular design with clear separation of concerns:

### Core Components

1. **Base Classes** (`base_boids.py`)
   - `BaseBoid`: Abstract base class defining core boid behavior
   - `BaseSpace`: Abstract space for managing boid populations
   - `CommunicationStrategy`: Protocol for data transmission between components

2. **Communication** (`pipe_boids.py`)
   - Implements pipe-based communication between simulation and visualization
   - Extensible to other communication methods

3. **Visualization**
   - Supports both Pygame (`boids_game.py`) and Matplotlib (`boids_animate.py`)
   - Visualization choice handled by runner

4. **Runner** (`boids_runner.py`)
   - CLI interface for launching simulation
   - Manages processes and communication setup

## How Everything Fits Together

1. The runner creates two processes:
   - Generator process: Runs the boid simulation
   - Visualization process: Displays the simulation

2. Data flow:
   ```
   Space → Communication Strategy → Pipe → visualiser
   ```

3. Each frame:
   - Boids update their positions
   - States are written to communication channel
   - visualiser reads and displays the new states

## Extending the System

### Adding New Communication Methods

1. Create a new class implementing `CommunicationStrategy`
2. Implement required methods:
   - `write_state(state: BoidState)`
   - `write_frame_end()`
   - `cleanup()`

Example:
```python
class NetworkCommunication(CommunicationStrategy):
    def write_state(self, state: BoidState) -> None:
        # Send state over network
        pass
```

### Adding New Visualizations

1. Create a new visualiser class
2. Implement frame reading and display logic
3. Add new option to runner CLI

### Modifying Boid Behavior

1. Inherit from `BaseBoid`
2. override movement methods
   - `move()`
   OR override the movement helpers
   - `move_together()`
   - `move_away()`
   - `handle_edges()`

### Adding New Parameters

1. Add parameters to `parameters.py`
2. Use in relevant boid or space classes

## Best Practices

1. Always inherit from base classes for consistency
2. Use type hints and documentation
3. Follow the existing communication protocol
4. Keep visualization logic separate from simulation logic


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
