import logging
import logging.handlers
import multiprocessing

def setup_worker_logging(queue, logger_name=None, level=logging.DEBUG):
    """
    Setup logging for a worker process to send logs to a queue

    Args:
        queue: The multiprocessing queue to send log records to
        logger_name: The name of the logger for the worker
    """
    if logger_name is None:
        logger_name = multiprocessing.current_process().name
    worker_logger = logging.getLogger(logger_name)
    worker_logger.setLevel(level)
    # Remove all existing handlers to avoid duplicate logs
    for handler in list(worker_logger.handlers):
        worker_logger.removeHandler(handler)
    h = logging.handlers.QueueHandler(queue)
    worker_logger.addHandler(h)
    worker_logger.propagate = False  # Prevent double logging
    return worker_logger

def listener_configurer():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    # Remove all existing handlers to avoid duplicate logs
    for handler in list(root.handlers):
        root.removeHandler(handler)
    h = logging.StreamHandler()
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)
    root.propagate = False

def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

def start_logging_proc():
    """
    Start a proc that listens for log messages in a multiprocessing queue and logs them to console
    """
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                        args=(queue, listener_configurer),
                                        daemon=True)
    listener.start()
    return queue, listener

def stop_logging_proc(queue, listener, timeout=3):
    """
    Stop the logging listener process cleanly.
    """
    if queue is not None:
        try:
            queue.put_nowait(None)
        except Exception:
            pass
    if listener is not None and listener.is_alive():
        listener.join(timeout=timeout)
