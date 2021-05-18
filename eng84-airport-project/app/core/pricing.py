from .vars import AIRPLANE_SPEED


def cost_of_flight_per_hour(weight):
    return weight*0.1


def cost_of_flight(weight, distance):
    return cost_of_flight_per_hour(weight)*(distance / AIRPLANE_SPEED)
