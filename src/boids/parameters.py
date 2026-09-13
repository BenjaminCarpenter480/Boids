import yaml
import logging
from dataclasses import dataclass

@dataclass
class Parameters:

    def __init__(self, file_path: str = "parameters/default.yaml"):
        with open(file_path, "r") as f:
            loaded_parameters = yaml.safe_load(f) or {}

        self.logger = logging.getLogger("boids.parameters")
        self._fps = loaded_parameters.get("fps", 1/60)
        self.logger.debug(f"FPS: {self._fps}")
        self._pipe = loaded_parameters.get("pipe", "/tmp/boids_pipe")
        self.logger.debug(f"Pipe: {self._pipe}")
        self._num_boids = loaded_parameters.get("num_boids", 50)
        self.logger.debug(f"Num boids: {self._num_boids}")
        self._step_size = loaded_parameters.get("step_size", 1)
        self.logger.debug(f"Step size: {self._step_size}")
        self._move_random_probability = loaded_parameters.get("move_random_probability", 0.6)
        self.logger.debug(f"Move random probability: {self._move_random_probability}")
        self.domain = loaded_parameters.get("domain", 8000)
        self.logger.debug(f"Domain: {self._domain}")
        self._turn_speed = loaded_parameters.get("turn_speed", 1)
        self.logger.debug(f"Turn speed: {self._turn_speed}")
        self._randomness_factor = loaded_parameters.get("randomness_factor", 20)
        self.logger.debug(f"Randomness factor: {self._randomness_factor}")
        self._move_away_factor = loaded_parameters.get("move_away_factor", 0.4)
        self.logger.debug(f"Move away factor: {self._move_away_factor}")
        self._visual_dist = loaded_parameters.get("visual_dist", 500)
        self.logger.debug(f"Visual distance: {self._visual_dist}")
        self._avoid_dist = loaded_parameters.get("avoid_dist", 400)
        self.logger.debug(f"Avoid distance: {self._avoid_dist}")
        self._min_separation = loaded_parameters.get("min_separation", 150)
        self.logger.debug(f"Minimum separation: {self._min_separation}")
        self._match_speed_factor = loaded_parameters.get("match_speed_factor", 0.6)
        self.logger.debug(f"Match speed factor: {self._match_speed_factor}")
        self._centering_factor = loaded_parameters.get("centering_factor", 0)
        self.logger.debug(f"Centering factor: {self._centering_factor}")
        self._max_speed = loaded_parameters.get("max_speed", 50)
        self.logger.debug(f"Max speed: {self._max_speed}")
        self._min_speed = loaded_parameters.get("min_speed", 1)

    @property
    def fps(self)-> float:
        return self._fps

    @property
    def pipe(self)-> float:
        return self._pipe

    @property
    def num_boids(self)-> float:
        return self._num_boids

    @property
    def step_size(self)-> float:
        return self._step_size

    @property
    def move_random_probability(self)-> float:
        return self._move_random_probability

    @property
    def domain(self)-> float:
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value
        self.logger.debug(f"Domain: {self._domain}")
        self._left_margin = 0
        self.logger.debug(f"Left margin: {self._left_margin}")
        self._right_margin = self.domain
        self.logger.debug(f"Right margin: {self._right_margin}")
        self._bottom_margin = self.domain
        self.logger.debug(f"Bottom margin: {self._bottom_margin}")
        self._top_margin = 0
        self.logger.debug(f"Top margin: {self._top_margin}")

    @property
    def turn_speed(self)-> float:
        return self._turn_speed

    @property
    def randomness_factor(self)-> float:
        return self._randomness_factor

    @property
    def left_margin(self)-> float:
        return self._left_margin

    @property
    def right_margin(self)-> float:
        return self._right_margin

    @property
    def bottom_margin(self)-> float:
        return self._bottom_margin

    @property
    def top_margin(self)-> float:
        return self._top_margin

    @property
    def move_away_factor(self)-> float:
        return self._move_away_factor

    @property
    def visual_dist(self)-> float:
        return self._visual_dist

    @property
    def avoid_dist(self)-> float:
        return self._avoid_dist

    @property
    def min_separation(self)-> float:
        return self._min_separation

    @property
    def match_speed_factor(self)-> float:
        return self._match_speed_factor

    @property
    def centering_factor(self)-> float:
        return self._centering_factor

    @property
    def max_speed(self)-> float:
        return self._max_speed

    @property
    def min_speed(self)-> float:
        return self._min_speed
