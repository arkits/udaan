from loguru import logger
import numpy


def calculateTrajectory(startPort, endPort):

    trajectory = []

    latTrajectory = calculateTrajectoryPoints(startPort, endPort, "latDeg")
    lonTrajectory = calculateTrajectoryPoints(startPort, endPort, "lonDeg")

    for x in range(len(latTrajectory)):

        trajectory.append({
            'latDeg': latTrajectory[x],
            'lonDeg': lonTrajectory[x]
        })

    return trajectory


def calculateTrajectoryPoints(startPort, endPort, coType):

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
    for rPoint in numpy.linspace(pointA, pointB, 30):

        trajectoryPts.append(rPoint)

    if reversePts:

        trajectoryPts.reverse()

    return trajectoryPts
