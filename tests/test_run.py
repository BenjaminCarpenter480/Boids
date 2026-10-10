import subprocess
import time
import signal
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


def test_boids_cli_help():
    """Verify package CLI entrypoint shows help."""
    res = subprocess.run(
        ["uv", "run", "boids", "--help"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert res.returncode == 0
    assert "Usage: boids" in res.stdout
    assert "matplotlib" in res.stdout


def test_boid_runner_help():
    """Verify root boid_runner.py script shows help."""
    res = subprocess.run(
        ["uv", "run", "boid_runner.py", "--help"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert res.returncode == 0
    assert "Usage: boid_runner.py" in res.stdout
    assert "matplotlib" in res.stdout


def test_run_matplotlib_simulation_smoke():
    """Verify a simulation run initializes and executes without pickling or multiprocessing errors."""
    cmd = ["uv", "run", "boid_runner.py", "matplotlib"]
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        time.sleep(1.5)
        if proc.poll() is None:
            # Active GUI loop; trigger shutdown
            proc.send_signal(signal.SIGINT)
            stdout, stderr = proc.communicate(timeout=5)
        else:
            # Headless backend exits immediately after show()
            stdout, stderr = proc.communicate()
            assert proc.returncode == 0, f"Process exited with error code {proc.returncode}"
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        raise AssertionError(f"Simulation did not stop within timeout. stderr: {stderr}")

    assert "PicklingError" not in stderr, f"Encountered pickling error in stderr: {stderr}"
    assert "AttributeError" not in stderr, f"Encountered attribute error in stderr: {stderr}"
