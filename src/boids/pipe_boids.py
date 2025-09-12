import os
import logging
from random import randint, random
from typing import BinaryIO

from base_boids import BaseBoid, BaseSpace, BoidState, CommunicationStrategy
from parameters import Parameters as params

import debugpy
debugpy.debug_this_thread()


class PipeCommunication(CommunicationStrategy):
    """Pipe-based communication strategy"""
    def __init__(self) -> None:
        self.pipe: BinaryIO | None = None
        self._setup_pipe()

    def _setup_pipe(self) -> None:
        try:
            os.remove(params.PIPE)
        except FileNotFoundError:
            pass

        try:
            os.mkfifo(params.PIPE)
            self.pipe = open(params.PIPE, 'wb')
            logging.info("Pipe created and opened")
        except OSError as e:
            logging.error("Error with pipe: %s", str(e))
            raise

    def write_state(self, state: BoidState) -> None:
        if self.pipe:
            self.pipe.write(
                bytes(f'{state.x},{state.y},{state.vx},{state.vy};', 'ASCII')
            )

    def write_frame_end(self) -> None:
        if self.pipe:
            self.pipe.write(bytes("\n", 'ASCII'))

    def cleanup(self) -> None:
        if self.pipe:
            self.pipe.close()
        try:
            os.remove(params.PIPE)
        except FileNotFoundError:
            pass

class PipeSpace(BaseSpace):
    """Space implementation using pipe communication"""
    def _initialize_boids(self) -> None:
        # First, create boids with a placeholder for the boid list
        self.boid_list = [
            PipeBoid(
                [],
                randint(1, params.DOMAIN),
                randint(1, params.DOMAIN),
                random(),
                random()
            ) for _ in range(params.NUM_BOIDS)
        ]
        # Now assign the full boid list to each boid
        for boid in self.boid_list:
            boid._boids = self.boid_list

class PipeBoid(BaseBoid):
    """Boid implementation for pipe communication.

    Inherits all functionality from BaseBoid; no additional behavior is defined here.
    """