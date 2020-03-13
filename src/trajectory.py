from loguru import logger
import numpy
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0


def calculateTrajectory(flight):

    startPort = flight["startPort"]
    endPort = flight["endPort"]
    cruiseSpeed = flight["cruiseSpeed"]

    trajectory = []

    distanceKm = calculateDistance(startPort, endPort)

    timeS = (distanceKm / cruiseSpeed) * 60 * 60
    logger.info("Calculated timeS - {}", timeS)

    timeTaken = int(timeS)

    latTrajectory = calculateTrajectoryPoints(
        startPort, endPort, "latDeg", timeTaken)
    lonTrajectory = calculateTrajectoryPoints(
        startPort, endPort, "lonDeg", timeTaken)

    for x in range(len(latTrajectory)):

        trajectory.append({
            'latDeg': latTrajectory[x],
            'lonDeg': lonTrajectory[x]
        })

    return trajectory


def calculateTrajectoryPoints(startPort, endPort, coType, timeTaken):

    trajectoryPts = []

    pointA = None
    pointB = None

    reversePts = False

    if startPort[coType] < endPort[coType]:
        pointA = startPort[coType]
        pointB = endPort[coType]

    else:
        pointB = startPort[coType]
        pointA = endPort[coType]

        reversePts = True

    # TODO: Calculate step based on distance
    for rPoint in numpy.linspace(pointA, pointB, timeTaken):

        trajectoryPts.append(rPoint)

    if reversePts:

        trajectoryPts.reverse()

    return trajectoryPts


def calculateDistance(startPort, endPort):

    lat1 = radians(startPort["latDeg"])
    lon1 = radians(startPort["lonDeg"])

    lat2 = radians(endPort["latDeg"])
    lon2 = radians(endPort["lonDeg"])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c     # In km

    return distance
