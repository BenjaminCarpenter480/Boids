import time
import typer
import multiprocessing

import boids_gen
import boids_game

boids_app = typer.Typer(name="boids", add_completion=False)

@boids_app.command()
def startup():
    """
    Run the boids simulation with the default parameters and visulization
    """
    typer.echo("Running boids")
    space = boids_gen.Space()

    generator_proc = multiprocessing.Process(target=space.startup())
    generator_proc.start()
    time.sleep(1)
    visulisation = boids_game.Game_Space()
    visulisation_proc = multiprocessing.Process(visulisation.loop())
    visulisation_proc.start()
    while True:
        if (not generator_proc.is_alive() or
            not visulisation_proc.is_alive()):
            visulisation_proc.terminate()
            generator_proc.terminate()
            break

if __name__ == "__main__":
    boids_app()
