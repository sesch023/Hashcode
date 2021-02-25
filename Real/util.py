from collections import defaultdict, deque


class Street(object):
    start_int = 0
    end_int = 0
    street_name = ""
    time_length = 0
    green_time = 0

    car_queue = deque()

    def __str__(self):
        return f"({str(self.start_int)}, {str(self.end_int)}, {self.street_name}, " \
               f"{str(self.time_length)}, {str(self.green_time)})"


class CarPath(object):
    path_length = 0
    streets = []

    def __str__(self):
        street_string = ""

        for element in self.streets:
            street_string += str(element) + ", "

        return f"{str(self.path_length)}, [{street_string}]"


class Intersection(object):
    outgoing_streets = []
    incomming_streets = []


class StreetMap(object):
    current_duraction = 0
    duration = 0
    intersect_num = 0
    num_streets = 0
    num_cars = 0
    points_per_Car = 0

    streets = {}
    nodes = defaultdict(Intersection)

    car_paths = []

    def __str__(self):
        street_string = ""
        for element in self.streets:
            street_string += str(element) + " "

        car_string = ""

        for element in self.car_paths:
            car_string += str(element) + "\n"

        return f"{str(self.duration)}, {str(self.intersect_num)}, {self.num_streets}, " \
               f"{str(self.num_cars)}, {str(self.points_per_Car)} \n [{street_string}] \n " \
               f"{str(self.nodes)} \n [{car_string}]"

    def start_simulation(self):



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

            streetmap.nodes[street_obj.end_int].incomming_streets.append(street_obj)
            streetmap.nodes[street_obj.start_int].outgoing_streets.append(street_obj)

            streetmap.streets[street_obj.street_name] = street_obj
            street_count += 1

        car_count = 0
        while car_count < streetmap.num_cars:
            car = file.readline()[:-1].split(" ")
            car_obj = CarPath()
            car_obj.path_length = car[0]

            for street_name in car[1:]:
                car_obj.streets.append(streetmap.streets[street_name])

            streetmap.car_paths.append(car_obj)
            car_count += 1

    return streetmap


print(read_file("files/a.txt"))
