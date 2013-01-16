import sys, time
from daemon import Daemon
import requests

MOCK_RPI = True

TASK_SERVICE_URL = 'http://localhost:5000'
CHECK_FOR_NEW_EVENTS_INTERVAL = 5
NULL_EVENT = {'valve':0,'duration':0,'start_time':0,'command':0}

STOP_COMMAND = 1
MANUAL_RUN_COMMAND = 2

__all__ = ['ValveController']

def _get_next_priority_event():
    r = requests.post(TASK_SERVICE_URL + '/next/priority')
    return r.json()

def _get_next_event():
    r = requests.post(TASK_SERVICE_URL + '/next/event')
    return r.json()
    
def _open_valve(valve_id=None):

    if MOCK_RPI:
        print "Valve " + repr(valve_id) + " is open..."
        return

def _close_valve(valve_id=None):

    if MOCK_RPI:
        print "Valve " + repr(valve_id) + " is closed..."
        return

def _close_all_valves():
    pass

class ValveController(Daemon):

    def run(self):

        next_event = None

        while True:

            time.sleep(5)

            if (next_event == None):
                current_event = _get_next_event()

            if (cmp(current_event, NULL_EVENT) != 0):
                run_time = int(current_event['duration']) * 60
                valve_id = _open_valve(current_event['valve'])
            else:
                run_time = 0

                while run_time > 0:
                    run_time = run_time - 5
                    time.sleep(5)
                    priority_event = _get_next_priority_event()

                    # Continue as normal
                    if (cmp(priority_event, NULL_EVENT) == 0):
                        next_event = None

                    # Need to interrupt the current event
                    if (cmp(priority_event, NULL_EVENT) != 0):
                        valve_id = _close_valve(current_event)
                        current_event = priority_event
                        next_event == priority_event
                        break
        

