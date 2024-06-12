import json
import random
from itertools import combinations

# 2.1 Partie 1 : manipulation des données
def read_file(filename):
    """Reads sensor configuration from a file."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError:
        print("File not found or error in reading file.")
        return None

    sensor_count = int(lines[0].strip())
    print('sensor_count', sensor_count)
    zone_count = int(lines[1].strip())
    print('zone_count', zone_count)
    time_data = list(map(int, lines[2].strip().split()))
    print('time_data', time_data)

    zone_data = []
    for i in range(3, 3 + sensor_count):
        zone_data.append(lines[i].strip().split())

    return sensor_count, zone_count, time_data, zone_data

# 2.1 Partie 1 : manipulation des données
def user_input_loop():
    """Gathers user input for sensor configuration."""
    print("You will start entering manual data.")
    scanner_count = int(input("Enter the number of scanners:\n"))
    zone_count = int(input("Enter the number of zones:\n"))
    time_list = input("Enter lifespan of each scanner separated by space (e.g., '6 3 2 6'):\n")
    time_data = list(map(int, time_list.split()))

    print("Enter zones covered by each scanner in format: z1 z2 (e.g., '1 2')")
    zone_data = []
    for i in range(scanner_count):
        zones = input(f"Scanner {i + 1}: ").split()
        zone_data.append(zones)

    return scanner_count, zone_count, time_data, zone_data

# 2.2 Partie 2 : construction de configurations élémentaires
def find_elementary_configurations(scanner_count, zone_count, zone_data):
    """Finds all configurations of scanners that cover all zones.
    Brute force approach"""
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


