# Inputs: car sensed at x traffic light, data of all the roads (length, width, location, speed limit),
#         intersections (each with 4 lights),

# Outputs: When and what traffic light to turn off


# class Light:
#
#     def __init__(self, direction, state):
#         self.direction = direction
#         self.state = state
#
#     def changeState(st8):
#         state = st8


class Intersection:

    def __init__(self, x, y, numLights, ID):
        self.x = x
        self.y = y
        self.numLights = numLights
        self.ID = ID


class Street:

    def __init__(self, speedLimit, inter1, inter2):
        self.speedLimit = speedLimit
        self.length = (inter2.x - inter1.x) + (inter2.y - inter1.x)  # distance between