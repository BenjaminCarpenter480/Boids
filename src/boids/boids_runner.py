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

def run_animation():
    visulisation =  bv.BoidVisualiser()
    visulisation.animate()

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
            visulisation_proc = multiprocessing.Process(target=run_animation)
            visulisation_proc.start()
            while ((vis_alive := visulisation_proc.is_alive())
                    and (gen_alive := generator_proc.is_alive())):
                time.sleep(0.1)
            if (not vis_alive):
                logger.info("Visulization proc ended")
                generator_proc.terminate()
                generator_proc.join()
            if (not gen_alive):
                logger.info("Generator proc ended")
                visulisation_proc.terminate()
                visulisation_proc.join()
    except KeyboardInterrupt:
        generator_proc.terminate()
        generator_proc.join()

if __name__ == "__main__":
    boids_app()
