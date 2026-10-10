"""Boids simulation package."""
from boids.boids_runner import boids_app

def main() -> None:
    """CLI entrypoint for boids simulation."""
    boids_app()

__all__ = ["main", "boids_app"]
