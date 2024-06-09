import json
import random
from itertools import combinations

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    scanner_count = int(lines[0].strip())
    zone_count = int(lines[1].strip())
    
    time_data = list(map(int, lines[2].strip().split()))

    zone_data = []
    for i in range(3, 3 + scanner_count):
        zone_data.append(list(map(str, lines[i].strip().split())))

    return scanner_count, zone_count, time_data, zone_data

def user_input_loop():
    print("You will start entering manual data.")
    scanner_count = int(input("Enter the number of scanner :\n"))
    zone_count = int(input("Enter the number of zone :\n"))
    time_list = str(input("Enter all the time unit like 't1 t2 t3 t4' :\n"))
    time_data = time_list.split(' ')
    print("Please, respect the following format :")
    print("scanner x : z1 z2 z3 z4 (leur id)")
    zone_data = []
    for i in range(scanner_count):
        zone_data.append(str(input("scanner " + str(i) + " : ")).split())
    print(zone_data)
    print(time_data)
    return scanner_count, zone_count, time_data, zone_data

def find_elementary_configurations(scanner_count, zone_count, zone_data):
    elementary_configs = []

    # Generate all possible combinations of scanners
    for r in range(1, scanner_count + 1):
        for combo in combinations(range(scanner_count), r):
            covered_zones = set()
            for scanner_index in combo:
                covered_zones.update(zone_data[scanner_index])
            if len(covered_zones) == zone_count:
                elementary_configs.append(combo)
    return elementary_configs

def main(): 
    print("Sensor Activation Scheduling for Zone Surveillance")
    print("1. Read data from file")
    print("2. Generate random data")
    print("3. Enter data manually")
    choice = int(input("Choose an option (1/2/3): "))

    if choice == 1:
        filename = str(input("Enter relative filepath: "))
        scanner_count, zone_count, time_data, zone_data = read_file(filename)
        config = find_elementary_configurations(scanner_count, zone_count, zone_data)
        print("Elementary configurations:", config)
    elif choice == 2: 
        print("We'll see that later <3 !")
    elif choice == 3:
        scanner_count, zone_count, time_data, zone_data = user_input_loop()
        config = find_elementary_configurations(scanner_count, zone_count, zone_data)
        print("Elementary configurations:", config)

if __name__ == "__main__":
    main()


