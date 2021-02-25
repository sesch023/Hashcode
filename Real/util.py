class Street(object):
    start_int = 0
    end_int = 0
    street_name = ""
    time_length = 0


class CarPath(object):
    path_length = 0
    streets = []

class StreetMap(object):
    duration = 0
    intersect_num = 0
    num_streets = 0
    num_cars = 0
    points_per_Car = 0

    streets = []

    car_paths = []
