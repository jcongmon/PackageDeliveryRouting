# Jonathan Congmon
# 010318775
from datetime import datetime
from util import truck_1, truck_2, truck_3, run_delivery, mp


def run_deliveries(truck_a, truck_b, truck_c):
    """Initiates nearest neighbor algorithm on all trucks"""
    run_delivery(truck_a)
    run_delivery(truck_b)
    run_delivery(truck_c)


def enter_valid_id():
    """Checks for valid package ID and returns valid ID"""
    flag1 = True
    while flag1 is True:
        choice = int(input(f"Enter a valid package ID:\n"))
        if (choice <= 40) and (choice >= 1):
            flag1 = False
        else:
            continue
    return choice


def valid_time():
    """Checks for valid time input and returns time in seconds"""
    flag1 = True
    while flag1 is True:
        time_string = str(input(f"Enter a time (HH:MM:SS)\n"))
        try:
            time = datetime.strptime(time_string, '%H:%M:%S')
        except:
            print(f"That is not a valid time format.")
            continue
        time_seconds = int(time.second) + int(time.minute * 60) + int(time.hour * 3600)
        if time_seconds > 63000 or time_seconds < 28800:
            print(f"Our operating hours are from 8:00:00 to 17:30:00")
            continue
        else:
            return time_seconds


def get_package_status(package, time_seconds):
    """Prints status of package in relation to time in seconds"""
    print(f"Package ID: {mp.get_id(package)}\n"
          f"Delivery Address: {mp.get_address(package)}\n"
          f"City: {mp.get_city(package)}, State: {mp.get_state(package)}, Zip Code: {mp.get_zip(package)}\n"
          f"Deadline: {mp.get_deadline(package)}, Weight: {mp.get_weight(package)} kg\n"
          f"Notes: {mp.get_note(package)}")
    if time_seconds >= mp.get_time_seconds(package):
        if mp.get(package).address in truck_1.truck_path:
            truck_delivery = truck_1.name
        elif mp.get(package).address in truck_2.truck_path:
            truck_delivery = truck_2.name
        else:
            truck_delivery = truck_3.name
        print(f"Status: Delivered at {mp.get_delivery_time(package)} by {truck_delivery}\n")
    elif mp.get(package).address in truck_1.truck_path:
        if time_seconds < mp.get_time_seconds(package):
            print(f"Status: En route\n")
    elif mp.get(package).address in truck_2.truck_path:
        if time_seconds < 32700:
            print(f"Status: At hub\n")
        else:
            print(f"Status: En route\n")
    elif mp.get(package).address in truck_3.truck_path:
        if time_seconds < 37200:
            print(f"Status: At hub\n")
        else:
            print(f"Status: En route\n")


def get_all_packages(time_seconds):
    """Prints status of all packages at a designated time"""
    for package in range(1, 41):
        get_package_status(package, time_seconds)


def print_total_miles():
    """Prints total miles traveled of all trucks"""
    total_miles = round((truck_1.miles + truck_2.miles + truck_3.miles), 2)
    print(f"The total mileage of all trucks is {total_miles} miles\n"
          f"All packages were delivered on time.")


run_deliveries(truck_1, truck_2, truck_3)

flag = True
while flag is True:     # interface
    choice = input(
        f"=====================================\n"
        f"Welcome to the WGUPS tracking system.\n"
        f"1 - Get status of a package\n"
        f"2 - Get status of all packages at a certain time\n"
        f"3 - Get total mileage of all trucks\n"
        f"q - Exit program\n"
        f"=====================================\n"
    )

    if choice == '1':
        package_id = enter_valid_id()
        time_seconds = valid_time()
        get_package_status(package_id, time_seconds)
    elif choice == '2':
        time_seconds = valid_time()
        get_all_packages(time_seconds)
    elif choice == '3':
        print_total_miles()
    elif choice == ('q' or 'Q'):
        flag = False
        print("Thank you for using this service.")
    else:
        print("Enter a valid option.")
