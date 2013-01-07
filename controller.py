import sys, time
from daemon import Daemon

TASK_SERVICE_URL = 'http://localhost:5000/next/priority'

__all__ = ['ValveController']

def _get_next_priority_event():
    pass

def _get_next_event():
    pass

def _do_event():
    pass

class ValveController(Daemon):
    def __init__(self):
        pass

    def run(self):
        while True:

