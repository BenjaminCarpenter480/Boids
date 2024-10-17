import time
import multiprocessing
import logging
import typer

import boids_gen as bg
import boids_game as ba
import boids_animate as bv

boids_app = typer.Typer(name="boids", add_completion=False)

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)


@boids_app.command(name="pygame")
def run_with_pygame():
    boids_sim("pygame")


@boids_app.command(name="matplotlib")
def run_with_matplotlib():
    boids_sim("matplotlib")


def boids_sim(visualiser: str = "pygame"):
    """
    Run the boids simulation with the default parameters and visulization
    """
    logger = setup_logging()
    logger.info("Starting boids simulation")
    space = bg.Space()

    generator_proc = multiprocessing.Process(target=space.run_loop)
    generator_proc.start()
    time.sleep(2)

    logger.info("Starting visulization")

    try:
        if (visualiser=="pygame"):
            visulisation = ba.GameVisuliser()
            visulisation.loop()
        else:
            visulisation =  bv.BoidVisualiser()
            visulisation.animate()

    except KeyboardInterrupt:
        generator_proc.terminate()
        generator_proc.join()

if __name__ == "__main__":
    boids_app()
