import sys, time
from daemon import Daemon
import requests

TASK_SERVICE_URL = 'http://localhost:5000/next/priority'
CHECK_FOR_NEW_EVENTS_INTERVAL = 5
NULL_EVENT = {'valve':0,'duration':0,'start_time':0,'command':0}

STOP_COMMAND = 1
MANUAL_RUN_COMMAND = 2

__all__ = ['ValveController']

def _get_next_priority_event():
    pass

def _get_next_event():
    pass

def _open_valve():
    pass

def _close_valve():
    pass

class ValveController(Daemon):
    def __init__(self):
        pass

    def run(self):

        next_event = None

        while True:

            if (next_event == None):
                current_event = _get_next_event()

            if (current_event != NULL_EVENT):
                run_time = int(x['duration']) * 60
                valve_id = _open_valve(current_event['valve'])

                while run_time > 0:
                    run_time = run_time - 5
                    time.sleep(5)
                    priority_event = _get_next_priority_event()

                    # Continue as normal
                    if (priority_event == NULL_EVENT):
                        next_event = None

                    # Need to interrupt the current event
                    if (priority_event != NULL_EVENT):
                        valve_id = _close_valve(current_event)
                        current_event = priority_event
                        next_event == priority_event
                        break
        
            time.sleep(5)

