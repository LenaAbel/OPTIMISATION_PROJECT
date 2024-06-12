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

# Fonction pour lire les données des capteurs à partir d'un fichier
def read_sensor_data_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()  # Lire toutes les lignes du fichier
    except IOError:
        print(f"{bcolors.FAIL}Fichier introuvable ou erreur lors de la lecture du fichier.{bcolors.ENDC}")
        return None

    sensor_count = int(lines[0].strip())  # Nombre de capteurs
    zones_count = int(lines[1].strip())  # Nombre de zones
    lifetimes = list(map(int, lines[2].strip().split()))  # Durée de vie des capteurs
    zone_data = []
    for i in range(3, 3 + sensor_count):
        zone_data.append(list(map(int, lines[i].strip().split())))  # Zones couvertes par chaque capteur

    return sensor_count, zones_count, lifetimes, zone_data

# Fonction pour générer des données aléatoires pour les capteurs et les zones
def generate_random_data(sensor_count, zones_count):
    lifetimes = [random.randint(1, 10) for _ in range(sensor_count)]  # Durée de vie aléatoire pour chaque capteur
    # Générer des zones couvertes aléatoirement pour chaque capteur
    zone_data = [random.sample(range(1, zones_count + 1), random.randint(1, zones_count)) for _ in range(sensor_count)]
    return sensor_count, zones_count, lifetimes, zone_data

# Fonction pour saisir manuellement les données des capteurs et des zones
def manually_enter_data():
    sensor_count = int(input("Entrez le nombre de capteurs: "))
    zones_count = int(input("Entrez le nombre de zones: "))
    lifetimes = list(map(int, input("Entrez la durée de vie de chaque capteur (séparée par des espaces): ").split()))
    zone_data = []
    for i in range(sensor_count):
        zones = list(map(int, input(f"Entrez les zones couvertes par le capteur {i + 1} (séparées par des espaces): ").split()))
        zone_data.append(zones)
    return sensor_count, zones_count, lifetimes, zone_data

# Heuristique gloutonne pour sélectionner les capteurs
def greedy_configuration_sensors(zones, sensors):
    """
    Utilise une heuristique gloutonne pour identifier un ensemble de capteurs qui couvre toutes les zones spécifiées.
    La fonction sélectionne le capteur qui couvre le plus grand nombre de zones encore non couvertes à chaque itération.
    """
    uncovered_zones = set(zones)  # Ensemble des zones non couvertes
    selected_sensors = []  # Liste des capteurs sélectionnés

    while uncovered_zones:
        best_sensor, best_coverage = None, 0  # Initialiser le meilleur capteur et le nombre de zones qu'il couvre
        # Parcourir chaque capteur et ses zones couvertes pour trouver le meilleur choix
        for sensor, zone_data in sensors.items():
            effective_coverage = len(uncovered_zones.intersection(zone_data))
            if effective_coverage > best_coverage:
                best_sensor, best_coverage = sensor, effective_coverage

        if best_sensor:
            uncovered_zones.difference_update(sensors[best_sensor])  # Mettre à jour les zones non couvertes
            selected_sensors.append(best_sensor)  # Ajouter le meilleur capteur à la liste des capteurs sélectionnés

        if best_sensor is None:
            break  # Si aucun capteur ne peut être trouvé pour couvrir des zones supplémentaires, arrêter la boucle

    return selected_sensors

# Vérifier si une configuration est élémentaire
def is_elementary_configuration(zones, sensors, config):
    """
    Vérifie si la configuration donnée couvre toutes les zones et est élémentaire.
    C'est-à-dire, si l'enlèvement de tout capteur de cette configuration fait que certaines zones ne sont plus couvertes.
    """
    covered_zones = set()
    for sensor in config:
        covered_zones.update(sensors[sensor])  # Ajouter les zones couvertes par chaque capteur de la configuration

    if set(zones) != covered_zones:
        return False  # Si toutes les zones ne sont pas couvertes, la configuration n'est pas élémentaire

    for sensor in config:
        temp_config = config.copy()  # Créer une copie temporaire de la configuration
        temp_config.remove(sensor)  # Retirer un capteur de la copie
        temp_covered_zones = set()
        for s in temp_config:
            temp_covered_zones.update(sensors[s])  # Vérifier les zones couvertes sans ce capteur
        if set(zones) == temp_covered_zones:
            return False  # Si la couverture est la même sans ce capteur, la configuration n'est pas élémentaire

    return True

# Recuit simulé pour trouver une configuration élémentaire
def recuit_simule(zones, sensors, initial_config):
    """
    Utilise le recuit simulé pour trouver une configuration élémentaire optimale.
    """
    def get_neighbor(config):
        """
        Générer un voisin en ajoutant ou en supprimant un capteur de la configuration donnée.
        """
        neighbor = config.copy()
        if random.random() > 0.5 and len(config) > 1:
            neighbor.remove(random.choice(config))  # Supprimer un capteur aléatoirement
        else:
            available_sensors = set(sensors.keys()) - set(config)
            if available_sensors:
                neighbor.append(random.choice(list(available_sensors)))  # Ajouter un capteur disponible
        return neighbor

    def acceptance_probability(old_cost, new_cost, temperature):
        """
        Calculer la probabilité d'accepter un voisin en fonction de la température et des coûts.
        """
        if new_cost < old_cost:
            return 1.0  # Toujours accepter si le coût est inférieur
        return math.exp((old_cost - new_cost) / temperature)  # Calculer la probabilité d'accepter une solution pire

    def cost_function(config):
        """
        Fonction de coût pour une configuration donnée.
        """
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

# Recherche exhaustive pour trouver toutes les configurations élémentaires
def find_elementary_configurations_bruteforce(zones, sensors):
    """
    Trouve toutes les configurations élémentaires en utilisant une approche brute-force.
    """
    elementary_configs = []
    all_sensors = list(sensors.keys())
    for r in range(1, len(all_sensors) + 1):
        for comb in combinations(all_sensors, r):
            if is_elementary_configuration(zones, sensors, list(comb)):
                elementary_configs.append(list(comb))  # Ajouter les configurations élémentaires trouvées
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
