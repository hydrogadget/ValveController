from daemon import Daemon
import requests

import sys,time

try:
    import RPi.GPIO as GPIO
    MOCK_RPI = False
except ImportError:
    MOCK_RPI = True

TASK_SERVICE_URL = 'http://localhost:8000'
NULL_EVENT = {'valve':None,'duration':None,'start_time':None,'command':None}

STOP_COMMAND = 1
MANUAL_RUN_COMMAND = 2
SLEEP_DURATION = 5

__all__ = ['ValveController']

VALVES = [1,2,3,4]

def _setup(valves=[]):

    GPIO.setmode(GPIO.BCM)

    for valve in valves:
        GPIO.setup(valve, GPIO.OUT)
        close(valve)

def _cleanup():
    GPIO.cleanup()

def _get_next_priority_event():
    r = requests.post(TASK_SERVICE_URL + '/next/priority')
    return r.json()

def _get_next_event():
    r = requests.post(TASK_SERVICE_URL + '/next/event')
    return r.json()
    
def _open_valve(valve_id=None):

    if valve_id == None:
        return

    if MOCK_RPI:
        print "Valve " + repr(valve_id) + " is open..."
        return valve_id
    
    GPIO.output(valve_id, True)
    return valve_ud

def _close_valve(valve_id=None):

    if valve_id == None:
        return

    if MOCK_RPI:
        print "Valve " + repr(valve_id) + " is closed..."
        return valve_id

    GPIO.output(valve_id, False)
    return valve_id

def _close_all_valves():
    pass

class ValveController(object):

    def run(self):

        valve_setup(VALVES)

        next_event = None

        while True:

            time.sleep(SLEEP_DURATION)

            if (next_event == None):
                current_event = _get_next_priority_event()
                print "if stmt 1: " + repr(current_event)

                if (cmp(current_event,NULL_EVENT) == 0):
                    current_event = None
            
            if (current_event == None):
                current_event = _get_next_event()
                print "if stmt 2: " + repr(current_event)

            if (cmp(current_event, NULL_EVENT) != 0 and current_event['duration'] != 0):
                print "if stmt 3: " + repr(current_event)
                run_time = int(current_event['duration']) * 60
                valve_id = _open_valve(current_event['valve'])
            else:
                run_time = 0
                
            while run_time > 0:
                print "entering runloop and running for " + str(run_time)
                run_time = run_time - SLEEP_DURATION
                time.sleep(SLEEP_DURATION)
                priority_event = _get_next_priority_event()

                # Continue as normal
                if (cmp(priority_event, NULL_EVENT) == 0):
                    next_event = None
                    print "continue as normal schedule"

                # Need to interrupt the current event
                if (cmp(priority_event, NULL_EVENT) != 0):
                    print "interrupting current schedule"
                    valve_id = _close_valve(current_event['valve'])
                    current_event = priority_event
                    next_event = priority_event
                    break
            else:
                valve_id = _close_valve(current_event['valve'])
                next_event = None
                current_event = None

if __name__ == "__main__":
    x = ValveController()
    x.run()


