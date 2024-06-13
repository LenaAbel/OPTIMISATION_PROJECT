import pulp

# Créer un problème d'optimisation
lp = pulp.LpProblem("Sensor_Scheduling", pulp.LpMaximize)

# Variables de décision
t_u1 = pulp.LpVariable('t_u1', lowBound=0, cat='Continuous')
t_u2 = pulp.LpVariable('t_u2', lowBound=0, cat='Continuous')
t_u3 = pulp.LpVariable('t_u3', lowBound=0, cat='Continuous')
t_u4 = pulp.LpVariable('t_u4', lowBound=0, cat='Continuous')

# Fonction objectif
lp += t_u1 + t_u2 + t_u3 + t_u4, "Total_Active_Time"

# Contraintes
lp += t_u2 + t_u3 + t_u4 <= 6, "Battery_Life_s1"
lp += t_u1 + t_u2 <= 3, "Battery_Life_s2"
lp += t_u3 <= 2, "Battery_Life_s3"
lp += t_u1 + t_u4 <= 6, "Battery_Life_s4"

# Résoudre le problème
lp.solve()

# Récupérer les valeurs des variables
results = {
    't_u1': pulp.value(t_u1),
    't_u2': pulp.value(t_u2),
    't_u3': pulp.value(t_u3),
    't_u4': pulp.value(t_u4),
    'Total_active_time': pulp.value(lp.objective)
}

# Afficher les résultats
for key, value in results.items():
    print(f"{key} = {value}")

# Sauvegarder les résultats dans un fichier
with open("optimization_results.txt", "w") as f:
    for key, value in results.items():
        f.write(f"{key} = {value}\n")
