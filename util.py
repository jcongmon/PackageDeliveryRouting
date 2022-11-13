import csv
import math
from hashmap import HashMap


class Truck:
    def __init__(self, name, miles, location, hours, minutes, seconds):
        self.package_list = []
        self.truck_path = []
        self.name = name
        self.miles = miles
        self.location = location
        self.hours = hours
        self.min = minutes
        self.sec = seconds

    def add_package(self, package):
        """Adds package to truck package list"""
        self.package_list.append(package)

    def set_time(self, distance):
        """Sets hours, minutes, and seconds of truck"""
        total_time = ((distance / 18) * 3600) + \
                     self.sec + (self.min*60) + (self.hours*3600) # 18 is average speed of car; time in seconds
        self.sec = round((total_time % 60))
        self.min = round((total_time / 60) % 60)
        self.hours = math.floor(total_time / 3600)

    def get_miles(self):
        return self.miles

    def update_miles(self, miles):
        self.miles = round((self.miles + miles), 2)

    def remove_package(self):
        """Removes package from package list"""
        self.package_list.pop(0)

    def set_truck_path(self):
        """Utilizes nearest neighbor algorithm to determine optimal path"""
        self.truck_path = nearest_neighbor(self, self.location, unvisited=[], path=[])

    def sort_package_by_nearest_neighbor(self):
        """Sorts truck package list by address in truck path"""
        temp = []
        for address in self.truck_path:
            for package in self.package_list:
                if address == package.address and package not in temp:
                    temp.append(package)
                    continue
        self.package_list = temp


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight,
                 note, location='AT HUB', time='0', time_seconds=0):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.location = location
        self.delivery_time = time
        self.time_seconds = time_seconds

    def set_delivery_time(self, hr, min, sec):
        """Sets package delivery time and the total time in seconds"""
        self.time_seconds = hr*3600 + min*60 + sec
        self.delivery_time = str(f"{hr:02}:{min:02}:{sec:02}")
        self.location = 'DELIVERED'


with open('distances.csv') as data:
    df_distances = list(csv.reader(data))

with open('packages.csv') as data:
    df_packages = list(csv.reader(data))

mp = HashMap()
key = 1
for i in df_packages:  # building hashmap, inserting values as package objects
    current_package = Package(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    mp.insert(key, current_package)
    key += 1

truck_1 = Truck('Truck A', 0, '4001 South 700 East', 8, 0, 0)   # instantiating trucks with start times
truck_2 = Truck('Truck B', 0, '4001 South 700 East', 9, 5, 0)
truck_3 = Truck('Truck C', 0, '4001 South 700 East', 10, 20, 0)

# manually loading trucks
truck_1.add_package(mp.get(1))
truck_1.add_package(mp.get(7))
truck_1.add_package(mp.get(10))
truck_1.add_package(mp.get(13))
truck_1.add_package(mp.get(14))
truck_1.add_package(mp.get(15))
truck_1.add_package(mp.get(16))
truck_1.add_package(mp.get(19))
truck_1.add_package(mp.get(20))
truck_1.add_package(mp.get(21))
truck_1.add_package(mp.get(29))
truck_1.add_package(mp.get(30))
truck_1.add_package(mp.get(34))
truck_1.add_package(mp.get(39))
truck_1.add_package(mp.get(40))

truck_2.add_package(mp.get(3))
truck_2.add_package(mp.get(5))
truck_2.add_package(mp.get(6))
truck_2.add_package(mp.get(18))
truck_2.add_package(mp.get(23))
truck_2.add_package(mp.get(25))
truck_2.add_package(mp.get(26))
truck_2.add_package(mp.get(27))
truck_2.add_package(mp.get(28))
truck_2.add_package(mp.get(31))
truck_2.add_package(mp.get(32))
truck_2.add_package(mp.get(33))
truck_2.add_package(mp.get(35))
truck_2.add_package(mp.get(36))
truck_2.add_package(mp.get(37))
truck_2.add_package(mp.get(38))

truck_3.add_package(mp.get(2))
truck_3.add_package(mp.get(4))
truck_3.add_package(mp.get(8))
truck_3.add_package(mp.get(9))
truck_3.add_package(mp.get(11))
truck_3.add_package(mp.get(12))
truck_3.add_package(mp.get(22))
truck_3.add_package(mp.get(24))


def run_delivery(truck):
    """Utilizes a nearest neighbor algorithm; updates truck object and package object values"""
    truck.set_truck_path()
    truck.sort_package_by_nearest_neighbor()
    for location in truck.truck_path:
        distance = check_distance(location, truck.location)
        truck.set_time(distance)
        truck.update_miles(distance)
        truck.location = location
        truck.package_list[0].set_delivery_time(truck.hours, truck.min, truck.sec)
        truck.remove_package()
    return_wgu(truck, '4001 South 700 East', truck.location)


def nearest_neighbor(truck, location, unvisited, path):
    for package in truck.package_list:
        unvisited.append(package.address)
    next_neighbor(truck, location, unvisited, path)
    return path


def next_neighbor(truck, location, unvisited, path):
    """Returns next neighbor to list"""
    if len(unvisited) == 0:
        return
    min_distance = float('inf')
    next_location = unvisited[0]
    for address in unvisited:
        distance = check_distance(address, location)
        if distance <= min_distance:
            min_distance = distance
            next_location = address
    path.append(next_location)
    unvisited.remove(next_location)
    next_neighbor(truck, next_location, unvisited, path)


def return_wgu(truck, end, location):
    """Returns truck back to WGU"""
    distance = check_distance(end, location)
    truck.update_miles(distance)
    truck.set_time(distance)
    truck.location = location


def check_distance(target_location, current_location):
    """Returns distance to location from current location"""
    row = get_idx_by_location(current_location)
    col = get_idx_by_location(target_location)
    distance = df_distances[row - 1][col + 2]  # offset
    return float(distance)


def get_idx_by_location(location):
    """Helper function to check indicies in relation to addresses in the distances dataframe"""
    idx = 1
    for row in df_distances:
        if row[1] == location:
            return idx
        else:
            idx += 1