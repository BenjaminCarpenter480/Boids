import time
import os
from pathlib import Path
import sys
import threading

# Ensure src and src/boids are in sys.path
_root = Path(__file__).resolve().parent.parent
_src = _root / "src"
_boids = _src / "boids"
for _p in (str(_src), str(_boids)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import multiproc_logging
from pipe_boids import PipeCommunication, PipeReadHandler
from base_boids import BoidState
from boids_runner import boids_sim_thread_func
from parameters import Parameters as params


def test_multiproc_logging_lifecycle():
    """Verify logging process starts, receives messages, and stops cleanly under current start method."""
    queue, listener = multiproc_logging.start_logging_proc()
    assert listener.is_alive(), "Listener process should be running"

    worker_logger = multiproc_logging.setup_worker_logging(queue, "test.logger")
    worker_logger.info("Test message from test runner")

    # Give listener a moment to process
    time.sleep(0.1)

    multiproc_logging.stop_logging_proc(queue, listener, timeout=3)
    assert not listener.is_alive(), "Listener process should have stopped cleanly"


def test_pipe_communication_roundtrip(monkeypatch, tmp_path):
    """Verify pipe communication writes state and reader consumes it without hanging."""
    test_pipe = str(tmp_path / "test_pipe")
    monkeypatch.setattr(params, "PIPE", test_pipe)

    comm = None
    def create_writer():
        nonlocal comm
        comm = PipeCommunication()

    writer_thread = threading.Thread(target=create_writer)
    writer_thread.start()

    # Wait for FIFO creation before reader opens it
    deadline = time.time() + 3.0
    while not os.path.exists(test_pipe) and time.time() < deadline:
        time.sleep(0.02)
    assert os.path.exists(test_pipe), "FIFO pipe should be created"

    reader = PipeReadHandler(test_pipe)
    writer_thread.join(timeout=3)
    assert comm is not None, "PipeCommunication should initialize"

    state = BoidState(x=10.0, y=20.0, vx=1.5, vy=-2.5)
    comm.write_state(state)
    comm.write_frame_end()

    # Read data back
    line = reader.get_data()
    assert "10.0,20.0,1.5,-2.5;" in line

    # Cleanup writer and pipe
    comm.cleanup()


def test_generator_process_lifecycle():
    """Verify simulation process starts and terminates cleanly without pickling errors."""
    try:
        os.remove(params.PIPE)
    except OSError:
        pass

    queue, listener = multiproc_logging.start_logging_proc()
    proc = None
    try:
        proc = boids_sim_thread_func(queue)
        proc.start()
        assert proc.is_alive(), "Generator process should start without error"

        # Wait for FIFO creation by generator
        deadline = time.time() + 5.0
        while not os.path.exists(params.PIPE) and time.time() < deadline:
            time.sleep(0.02)
        assert os.path.exists(params.PIPE), "Generator should create FIFO pipe"

        reader = PipeReadHandler(params.PIPE)
        # Read at least one frame of data from the simulation
        data = reader.get_data()
        assert data and ";" in data, "Generator should produce valid boid state data"
        assert proc.is_alive(), "Generator process should be actively running"
    finally:
        if proc is not None:
            proc.terminate()
            proc.join(timeout=3)
            assert not proc.is_alive(), "Generator process should terminate cleanly"
        multiproc_logging.stop_logging_proc(queue, listener)
        try:
            os.remove(params.PIPE)
        except OSError:
            pass
