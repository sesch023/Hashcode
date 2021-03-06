from collections import defaultdict, deque
from random import randint

green_light_values = dict()

class Street(object):
    def __init__(self):
        self.start_int = 0
        self.end_int = 0
        self.street_name = ""
        self.time_length = 0
        self.green_time = randint(1, 6)
        self.current_green_time = self.green_time

        self.car_queue = deque()

    def __str__(self):
        return f"({str(self.start_int)}, {str(self.end_int)}, {self.street_name}, " \
               f"{str(self.time_length)}, {str(self.green_time)})"

    def __repr__(self):
        return self.__str__()


class CarPath(object):
    def __init__(self):
        self.path_length = 0
        self.streets = deque()
        self.current_position = None
        self.drive_time = 0

    def __str__(self):
        street_string = ""

        for element in self.streets:
            street_string += str(element) + ", "

        return f"{str(self.path_length)}, {str(self.drive_time)}, [{street_string}]"

    def __repr__(self):
        return self.__str__()


class Intersection(object):
    def __init__(self):
        self.outgoing_streets = []
        self.incomming_streets = []
        self.current_green = 0

    def __str__(self):
        return f"({str(self.outgoing_streets)}, {str(self.incomming_streets)}, {self.current_green}"

    def __repr__(self):
        return self.__str__()


class StreetMap(object):
    def __init__(self):
        self.longest_deques = {}
        self.current_duration = 0
        self.duration = 0
        self.intersect_num = 0
        self.num_streets = 0
        self.num_cars = 0
        self.points_per_Car = 0

        self.streets = {}
        self.nodes = defaultdict(Intersection)

        self.car_paths = []

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
        while self.current_duration < self.duration:
            for node in self.nodes.values():
                current_street = node.incomming_streets[node.current_green]
                if len(current_street.car_queue) and current_street.car_queue[0].drive_time == 0:
                    car = current_street.car_queue.popleft()
                    car.streets.popleft()
                    if len(car.streets) > 0:
                        next_street = car.streets[0]
                        car.current_position = next_street
                        car.drive_time = next_street.time_length
                        next_street.car_queue.append(car)

            for car in self.car_paths:
                if car.drive_time > 0:
                    car.drive_time -= 1

            for node in self.nodes.values():
                current_street_green = node.incomming_streets[node.current_green]
                if current_street_green.current_green_time <= 1:
                    node.current_green += 1
                    if node.current_green >= len(node.incomming_streets):
                        node.current_green = 0
                else:
                    current_street_green.current_green_time -= 1

            for street in self.streets.values():
                if len(street.car_queue) > max(int(streetmap.num_cars * 0.005), 4):
                    if green_light_values[street.street_name] < streetmap.duration:
                        green_light_values[street.street_name] = min(streetmap.duration, green_light_values[street.street_name] + int(streetmap.duration * 0.01))
                elif len(street.car_queue) == 0:
                    if green_light_values[street.street_name] > 1:
                        green_light_values[street.street_name] = max(1, green_light_values[street.street_name] - int(streetmap.duration * 0.05))

            if self.current_duration % 1000 == 0:
                print(self.current_duration)
                print("Cars Left: " + str(sum([1 for car in self.car_paths if len(car.streets) > 0])))

            self.current_duration += 1


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

            if street_obj.street_name in green_light_values:
                street_obj.green_time = green_light_values[street_obj.street_name]
                street_obj.current_green_time = green_light_values[street_obj.street_name]

            streetmap.nodes[street_obj.end_int].incomming_streets.append(street_obj)
            streetmap.nodes[street_obj.start_int].outgoing_streets.append(street_obj)

            streetmap.streets[street_obj.street_name] = street_obj
            street_count += 1

        if len(green_light_values) == 0:
            for street in streetmap.streets.values():
                green_light_values[street.street_name] = street.green_time

        car_count = 0
        while car_count < streetmap.num_cars:
            car = file.readline()[:-1].split(" ")
            car_obj = CarPath()
            car_obj.path_length = car[0]

            for street_name in car[1:]:
                car_obj.streets.append(streetmap.streets[street_name])

            car_obj.current_position = streetmap.streets[car[1]]
            car_obj.current_position.car_queue.append(car_obj)
            streetmap.car_paths.append(car_obj)
            car_count += 1

    return streetmap


def write_scores(path, streetmap):
    with open(path, "w") as file:
        file.write(str(len(streetmap.nodes)) + "\n")

        for i in range(len(streetmap.nodes)):
            file.write(str(i) + "\n")
            file.write(str(len(streetmap.nodes[i].incomming_streets)) + "\n")
            for street in streetmap.nodes[i].incomming_streets:
                file.write(street.street_name + " " + str(street.green_time) + "\n")


files = ["e.txt"]

for file in files:
    print(file)
    for i in range(100):
        streetmap = read_file("files/" + file)
        streetmap.start_simulation()
        write_scores("scores/" + file, streetmap)
    green_light_values = dict()

