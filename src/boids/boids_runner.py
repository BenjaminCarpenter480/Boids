import time
import multiprocessing
import logging
import typer

import boids_gen as bg
import boids_game as bv

boids_app = typer.Typer(name="boids", add_completion=False)

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

@boids_app.command()
def boids_sim():
    """
    Run the boids simulation with the default parameters and visulization
    """
    logger = setup_logging()
    logging.info("Starting boids simulation")
    space = bg.Space()

    generator_proc = multiprocessing.Process(target=space.startup)
    generator_proc.start()
    time.sleep(2)

    logger.info("Starting visulization")
    visulisation = bv.GameVisuliser()

    try:
        visulisation.loop()

    except KeyboardInterrupt:
        generator_proc.terminate()
        generator_proc.join()

if __name__ == "__main__":
    boids_app()
