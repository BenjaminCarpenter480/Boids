#!/usr/bin/env python3
"""Runner script for Boids simulation."""
import sys
from pathlib import Path

# Ensure src and src/boids are in sys.path
root_dir = Path(__file__).resolve().parent
src_dir = root_dir / "src"
boids_dir = src_dir / "boids"
for path in (str(boids_dir), str(src_dir)):
    if path not in sys.path:
        sys.path.insert(0, path)

from boids.boids_runner import boids_app

if __name__ == "__main__":
    boids_app()
