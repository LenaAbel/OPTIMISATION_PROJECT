import math
import random
import time
from itertools import combinations

# Classe pour les couleurs de console
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKRED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_sensor_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError:
        print(f"{bcolors.FAIL}Fichier introuvable ou erreur lors de la lecture du fichier.{bcolors.ENDC}")
        return None

    sensor_count = int(lines[0].strip())  # Lire le nombre de capteurs
    zones_count = int(lines[1].strip())  # Lire le nombre de zones
    lifetimes = list(map(int, lines[2].strip().split()))  # Lire les durées de vie des capteurs
    zone_data = []
    for i in range(3, 3 + sensor_count):
        zone_data.append(list(map(int, lines[i].strip().split())))  # Lire les zones couvertes par chaque capteur

    return sensor_count, zones_count, lifetimes, zone_data

def generate_random_data(sensor_count, zones_count):
    # Générer des durées de vie aléatoires pour les capteurs (de 1 à 10)
    lifetimes = [random.randint(1, 10) for _ in range(sensor_count)]
    # Générer des zones couvertes aléatoirement pour chaque capteur
    zone_data = [random.sample(range(1, zones_count + 1), random.randint(1, zones_count)) for _ in range(sensor_count)]
    return sensor_count, zones_count, lifetimes, zone_data

def manually_enter_data():
    sensor_count = int(input("Entrez le nombre de capteurs: "))
    zones_count = int(input("Entrez le nombre de zones: "))
    lifetimes = list(map(int, input("Entrez la durée de vie de chaque capteur (séparée par des espaces): ").split()))
    zone_data = []
    for i in range(sensor_count):
        zones = list(map(int, input(f"Entrez les zones couvertes par le capteur {i + 1} (séparées par des espaces): ").split()))
        zone_data.append(zones)
    return sensor_count, zones_count, lifetimes, zone_data

def greedy_configuration_sensors(zones, sensors):
    uncovered_zones = set(zones)  # Ensemble des zones non couvertes
    selected_sensors = []  # Liste des capteurs sélectionnés

    while uncovered_zones:
        best_sensor, best_coverage = None, 0  # Initialiser le meilleur capteur et sa couverture
        print(f"Zones non couvertes: {uncovered_zones}")
        for sensor, zone_data in sensors.items():
            # Calculer combien de zones non couvertes sont couvertes par ce capteur
            effective_coverage = len(uncovered_zones.intersection(zone_data))
            print(f"Capteur: {sensor}, Zones couvertes: {effective_coverage}")
            if effective_coverage > best_coverage:
                best_sensor, best_coverage = sensor, effective_coverage

        if best_sensor:
            uncovered_zones.difference_update(sensors[best_sensor])  # Mettre à jour les zones non couvertes
            print(f"Zones couvertes par le capteur sélectionné: {sensors[best_sensor]}")
            selected_sensors.append(best_sensor)  # Ajouter le capteur sélectionné
            print(f"Capteur sélectionné: {best_sensor}")

        if best_sensor is None:
            break

    return selected_sensors

def is_elementary_configuration(zones, sensors, config):
    covered_zones = set()
    for sensor in config:
        covered_zones.update(sensors[sensor])  # Ajouter les zones couvertes par chaque capteur de la configuration

    if set(zones) != covered_zones:
        return False  # Vérifier si toutes les zones sont couvertes

    for sensor in config:
        temp_config = config.copy()
        temp_config.remove(sensor)  # Créer une configuration temporaire sans ce capteur
        temp_covered_zones = set()
        for s in temp_config:
            temp_covered_zones.update(sensors[s])  # Couvrir les zones avec la configuration temporaire
        if set(zones) == temp_covered_zones:
            return False  # Vérifier si la configuration est toujours valide sans ce capteur

    return True

def recuit_simule(zones, sensors, initial_config):
    def get_neighbor(config):
        neighbor = config.copy()
        if random.random() > 0.5 and len(config) > 1:
            neighbor.remove(random.choice(config))  # Supprimer aléatoirement un capteur
        else:
            available_sensors = set(sensors.keys()) - set(config)
            if available_sensors:
                neighbor.append(random.choice(list(available_sensors)))  # Ajouter aléatoirement un capteur
        return neighbor

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0  # Toujours accepter une meilleure solution
        return math.exp((old_cost - new_cost) / temperature)  # Probabilité d'accepter une pire solution

    def cost_function(config):
        covered_zones = set()
        for sensor in config:
            covered_zones.update(sensors[sensor])
        return len(zones) - len(covered_zones)  # Coût basé sur le nombre de zones non couvertes

    current_config = initial_config
    best_config = initial_config
    temperature = 100.0
    cooling_rate = 0.99

    while temperature > 1.0:
        neighbor = get_neighbor(current_config)
        if is_elementary_configuration(zones, sensors, neighbor):
            current_cost = cost_function(current_config)
            neighbor_cost = cost_function(neighbor)
            if acceptance_probability(current_cost, neighbor_cost, temperature) > random.random():
                current_config = neighbor
                if neighbor_cost < cost_function(best_config):
                    best_config = neighbor
        temperature *= cooling_rate

    return best_config

def find_elementary_configurations_bruteforce(zones, sensors):
    elementary_configs = []
    all_sensors = list(sensors.keys())
    for r in range(1, len(all_sensors) + 1):
        for comb in combinations(all_sensors, r):
            if is_elementary_configuration(zones, sensors, list(comb)):
                elementary_configs.append(list(comb))  # Ajouter les configurations élémentaires
    return elementary_configs

def main():
    print(f"Choisissez l'option de saisie des données:")
    print(f"{bcolors.OKBLUE}1. Lire depuis un fichier{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}2. Générer des données aléatoires{bcolors.ENDC}")
    print(f"{bcolors.WARNING}3. Entrer des données manuellement{bcolors.ENDC}")

    choice = input(f"{bcolors.BOLD}Entrez votre choix (1, 2, ou 3): {bcolors.ENDC}")

    if choice == '1':
        filename = input(f"Entrez le nom du fichier: ")
        sensor_count, zones_count, lifetimes, coverage = read_sensor_data_from_file(filename)
    elif choice == '2':
        sensor_count = int(input(f"{bcolors.OKCYAN}Entrez le nombre de capteurs pour les données aléatoires: {bcolors.ENDC}"))
        zones_count = int(input(f"{bcolors.OKCYAN}Entrez le nombre de zones pour les données aléatoires: {bcolors.ENDC}"))
        sensor_count, zones_count, lifetimes, coverage = generate_random_data(sensor_count, zones_count)
    elif choice == '3':
        sensor_count, zones_count, lifetimes, coverage = manually_enter_data()
    else:
        print(f"{bcolors.FAIL}Choix non valide. Veuillez sélectionner 1, 2, ou 3.{bcolors.ENDC}")
        return

    sensors = {f's{i + 1}': coverage[i] for i in range(sensor_count)}
    zones = list(range(1, zones_count + 1))

    print(f"{bcolors.HEADER}Nombre de capteurs:{bcolors.ENDC} {sensor_count}")
    print(f"{bcolors.HEADER}Nombre de zones:{bcolors.ENDC} {zones_count}")
    print(f"{bcolors.HEADER}Durée de vie des capteurs:{bcolors.ENDC} {lifetimes}")
    print(f"{bcolors.HEADER}Zones couvertes par chaque capteur:{bcolors.ENDC} {coverage}")

    # Mesurer le temps d'exécution pour l'heuristique gloutonne
    start_time = time.perf_counter()
    greedy_config = greedy_configuration_sensors(zones, sensors)
    end_time = time.perf_counter()
    greedy_time_ns = (end_time - start_time) * 1e9
    greedy_time_s = end_time - start_time
    print(f"{bcolors.OKGREEN}Configuration élémentaire trouvée par Greedy:{bcolors.ENDC} {greedy_config}")
    print(f"{bcolors.OKGREEN}Temps d'exécution pour Greedy:{bcolors.ENDC} {greedy_time_ns:.2f} ns ({greedy_time_s:.6f} s)")

    # Mesurer le temps d'exécution pour le recuit simulé
    start_time = time.perf_counter()
    sa_config = recuit_simule(zones, sensors, greedy_config)
    end_time = time.perf_counter()
    sa_time_ns = (end_time - start_time) * 1e9
    sa_time_s = end_time - start_time
    print(f"{bcolors.OKCYAN}Configuration élémentaire trouvée par recuit simulé:{bcolors.ENDC} {sa_config}")
    print(f"{bcolors.OKCYAN}Temps d'exécution pour Recuit Simulé:{bcolors.ENDC} {sa_time_ns:.2f} ns ({sa_time_s:.6f} s)")

    # Mesurer le temps d'exécution pour la recherche exhaustive
    start_time = time.perf_counter()
    all_elementary_configs = find_elementary_configurations_bruteforce(zones, sensors)
    end_time = time.perf_counter()
    brute_force_time_ns = (end_time - start_time) * 1e9
    brute_force_time_s = end_time - start_time
    print(f"{bcolors.OKBLUE}Configurations élémentaires trouvées par Brute-force:{bcolors.ENDC} {all_elementary_configs}")
    print(f"{bcolors.OKBLUE}Temps d'exécution pour Brute-force:{bcolors.ENDC} {brute_force_time_ns:.2f} ns ({brute_force_time_s:.6f} s)")

if __name__ == "__main__":
    main()
