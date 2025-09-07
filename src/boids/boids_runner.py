from typing import Literal
import time
import multiprocessing
import logging
import typer

from pipe_boids import PipeSpace, PipeCommunication
import boids_game as ba
import boids_animate as bv

boids_app = typer.Typer(name="boids", add_completion=False)

@boids_app.command(name="pygame")
def run_with_pygame() -> None:
    """Run simulation with pygame visualiser"""
    boids_sim("pygame")

@boids_app.command(name="matplotlib")
def run_with_matplotlib() -> None:
    """Run simulation with matplotlib visualiser"""
    boids_sim("matplotlib")

def run_animation() -> None:
    """Run the animation loop"""
    visualiser = bv.BoidVisualiser()
    visualiser.animate()

def boids_sim_thread_func() -> multiprocessing.Process:
    """Create and return a Process to run the boids simulation"""
    def sim_target():
        comm = PipeCommunication()
        space = PipeSpace(comm)
        space.sim_loop()

    process = multiprocessing.Process(target=sim_target)
    return process

def boids_sim(visualiser: Literal["pygame", "matplotlib"]) -> None:
    """
    Run the boids simulation with the specified visualiser

    Args:
        visualiser: The visualization backend to use ("pygame" or "matplotlib")
    """
    logger = setup_logging()
    logger.info("Starting boids simulation")

    generator_proc = boids_sim_thread_func()
    generator_proc.start()
    time.sleep(2)

    logger.info("Starting visualization")

    try:
        if visualiser == "pygame":
            visualiser = ba.GameVisuliser()
            visualiser.loop()
        else:
            visualization_proc = multiprocessing.Process(target=run_animation)
            visualization_proc.start()

            while True:
                if not visualization_proc.is_alive():
                    logger.info("Visualization process ended")
                    generator_proc.terminate()
                    break
                if not generator_proc.is_alive():
                    logger.info("Generator process ended")
                    visualization_proc.terminate()
                    break
                time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Error during simulation: {e}")
    finally:
        if 'generator_proc' in locals() and generator_proc.is_alive():
            generator_proc.terminate()
            generator_proc.join()
        if 'visualization_proc' in locals() and visualization_proc.is_alive():
            visualization_proc.terminate()
            visualization_proc.join()

if __name__ == "__main__":
    boids_app()
