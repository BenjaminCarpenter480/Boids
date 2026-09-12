import os
import logging
from random import randint, random
from typing import BinaryIO
import queue
import threading

from base_boids import BaseBoid, BaseSpace, BoidState, CommunicationStrategy
from standard_boid import StandardBoid
from parameters import Parameters as params

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
            self.pipe.flush()

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

    Inherits all functionality from parents; no additional behavior is defined here.
    """
    
class PipeReadHandler():
    """
    For reading data from the generator object

    Data is returned as a string with each boid seperated by a ';' and each "," seperating the boid
    attributes in the form x,y,vx,vy
    """

    def __init__(self, pipe_address=params.PIPE) -> None:
        """Class to handle reading from the pipe
        """
        self.__pipe = open(pipe_address,"rb")
        self.__data = queue.Queue()
        self.__pipe_reader = threading.Thread(target=self.empty_pipe)
        self.__pipe_reader.start()

    def empty_pipe(self):
        """
        Read from the pipe and put the data in the queue to be accessed by the process
        """
        while self.__pipe.readable():
            self.__data.put(self.__pipe.readline())

    def get_data(self):
        """Data stored in the pipe
        """
        return self.__data.get().decode('ASCII')
