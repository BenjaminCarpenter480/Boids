from typing import Literal
import time
import multiprocessing
import multiproc_logging
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

def run_animation(logger_queue) -> None:
    """Run the animation loop"""
    multiproc_logging.setup_worker_logging(logger_queue, "boids.visualiser")
    visualiser = bv.BoidVisualiser()
    visualiser.animate()


def boids_sim_thread_func(logger_queue) -> multiprocessing.Process:
    """Create and return a Process to run the boids simulation"""
    def sim_target():
        multiproc_logging.setup_worker_logging(logger_queue, "boids.space")
        multiproc_logging.setup_worker_logging(logger_queue, "boids.boid")
        comm = PipeCommunication()
        space = PipeSpace(comm)
        space.sim_loop()
    process = multiprocessing.Process(target=sim_target)
    return process


def boids_sim(visualiser: Literal["pygame", "matplotlib"]) -> None:
    """Run the boids simulation with the specified visualiser"""
    logger_queue, logger_proc = multiproc_logging.start_logging_proc()
    runner_logger = multiproc_logging.setup_worker_logging(logger_queue, "boids.runner")
    runner_logger.info("Starting boids simulation")

    generator_proc = boids_sim_thread_func(logger_queue)
    generator_proc.start()
    time.sleep(2)

    runner_logger.info("Starting visualization")

    try:
        if visualiser == "pygame":
            visualiser_obj = ba.GameVisuliser()
            visualiser_obj.loop()
        else:
            visualization_proc = multiprocessing.Process(target=run_animation, args=(logger_queue,))
            visualization_proc.start()

            while True:
                if not visualization_proc.is_alive():
                    runner_logger.info("Visualization process ended")
                    break
                if not generator_proc.is_alive():
                    runner_logger.info("Generator process ended")
                    break
                time.sleep(0.25)
    except KeyboardInterrupt:
        runner_logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:  # pragma: no cover
        runner_logger.error(f"Error during simulation: {e}")
    finally:
        if generator_proc.is_alive():
            generator_proc.join(timeout=3)
        if 'visualization_proc' in locals() and visualization_proc.is_alive():
            visualization_proc.join(timeout=3)

if __name__ == "__main__":
    boids_app()
