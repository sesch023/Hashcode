from collections import defaultdict

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

    streets = {}
    nodes = defaultdict(dict)

    car_paths = []


def read_file(file_path):
    streetmap = StreetMap()

    with open(file_path) as file:
        head = list(map(int, file.readline().split(" ")))
        streetmap.duration = head[0]
        streetmap.intersect_num = head[1]
        streetmap.num_streets = head[2]
        streetmap.num_cars = head[3]
        streetmap.points_per_Car = head[4]

        street_count = 0
        while street_count < streetmap.num_streets:
            street = file.readline()[:-1].split(" ")
            street_obj = Street()

            street_obj.start_int = int(street[0])
            street_obj.end_int = int(street[1])
            street_obj.street_name = street[2]
            street_obj.time_length = int(street[3])

            streetmap.streets[street_obj.street_name] = street_obj
            street_count += 1

        car_count = 0
        while car_count < streetmap.num_cars:
            car = file.readline()[:-1].split(" ")
            car_obj = CarPath()
            car_obj.path_length = car[0]

            for street_name in car[1:]:
                car_obj.streets.append(streetmap.streets[street_name])

            car_count += 1

    return streetmap

read_file("files/a.txt")
