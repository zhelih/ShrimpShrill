#!flask/bin/python

URL_PULL = "http://localhost:5000/ers/next_pending"
URL_PUSH = "http://localhost:5000/ers/approve/{}"

import sys
import signal
import requests
import json
import time
import random

def signal_handler(signal, frame):
    print "Got Ctrl+C, bye\n"
    sys.exit(0)

def parsePending(pending):
    if not "location" in pending:
        return
    
    URL  = URL_PUSH.format(pending['id'])
    data = {"level": random.randint(1, 3), "approved": int(time.time())}
    header = {'content-type': 'application/json'}
    response = requests.post(URL, data = json.dumps(data), headers = header);

def getPendingGenerator():
    def _():
        while True:
            response = requests.post(URL_PULL);
            yield response.json()
    return _()

def run(timeout = 5):
    generator = getPendingGenerator();
    while True:
        pending = generator.next()
        if pending and pending.get('ok', True):
            parsePending(pending)
        else:
            print "Queue is empty"
        time.sleep(timeout)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    run(timeout = int(sys.argv[1]))
