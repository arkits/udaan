from loguru import logger
import json
import socketio
import datetime
import time
import numpy
import threading
import trajectory as trajectoryUtil

sio = socketio.Client()

SFO = {
    "latDeg": 37.6213129,
    "lonDeg": -122.3789554
}

LAX = {
    "latDeg": 33.9415933,
    "lonDeg": -118.4107187
}

SJC = {
    "latDeg": 37.3639472,
    "lonDeg": -121.9289375
}


@sio.event
def connect():
    logger.info("Connected to Server")


def main():

    logger.info("Namaskar Mandali!")

    sio.connect('http://localhost:8786')

    trajectories = []

    flights = [
        {
            'callsign': "ARKITS1",
            'startPort': SFO,
            'endPort': SJC
        },
        {
            'callsign': "ARKITS2",
            'startPort': SJC,
            'endPort': SFO
        }
    ]

    for flight in flights:
        trajectory = trajectoryUtil.calculateTrajectory(
            flight['startPort'], flight['endPort'])
        trajectories.append(trajectory)

    flightThreads = []

    for x in range(len(flights)):

        flight = flights[x]
        trajectory = trajectories[x]

        flightThread = threading.Thread(
            target=flyFlight, args=(flight, trajectory,))

        flightThread.start()

        flightThreads.append(flightThread)

    for flightThread in flightThreads:
        flightThread.join()


def flyFlight(flight, trajectory):

    for trajectoryPoint in trajectory:

        flyVehicle(flight, trajectoryPoint)

        time.sleep(1)


def flyVehicle(flight, trajectoryPoint):

    payload = {
        'data': {
            'vid': flight['callsign'],
            'latDeg': trajectoryPoint['latDeg'],
            'lonDeg': trajectoryPoint['lonDeg']
        },
        'metadata': {
            'sourceTimestamp': str(datetime.datetime.utcnow().isoformat())
        }
    }

    logger.info("Emitting - {}", payload)

    sio.emit('brodcast_position', payload)


if __name__ == '__main__':
    main()
