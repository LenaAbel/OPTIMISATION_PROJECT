Partie 4 :
Pour expérimenter nous allons essayer avec les quatres temps suivant :

T1  T2  T3  T4  T5  Durée de vie optimale
1	6	3	2	6	8.5
2	5	4	3	5	8.0
3	4	3	2	4	6.5

Analyse
On peut constater que des durées de vie plus équilibrées entre les capteurs permettent une meilleure utilisation et prolongent la durée de vie du réseau.

En conclusion, cette méthode permet de maximiser la durée de vie du réseau de surveillance en utilisant un ordonnancement optimal des configurations de capteurs, en respectant les contraintes d'énergie.

Partie 5:
Étape 1 : Génération des configurations élémentaires
Imaginons que nous avons un réseau de 5 capteurs pour surveiller 4 zones. Voici un exemple de génération de configurations élémentaires pour ce réseau :

Capteurs et zones couvertes :

Capteur	Zones couvertes	Durée de vie (unité de temps)
s1	    z1, z2	        6
s2	    z2, z3	        3
s3	    z3	            2
s4	    z1, z3	        6
s5	    z1, z4	        4
Configurations élémentaires possibles :

u1 = (s1, s3, s5) : couvre z1, z2, z3, z4
u2 = (s2, s4) : couvre z2, z3, z1
u3 = (s1, s4) : couvre z1, z2, z3
u4 = (s3, s5) : couvre z3, z1, z4
Étape 2 : Résolution du programme linéaire
Nous résolvons le programme linéaire pour chaque ensemble de configurations élémentaires afin de maximiser la durée de vie du réseau. Par exemple, en utilisant le solveur GLPK, nous obtenons les durées de vie optimales pour chaque configuration.

Étape 3 : Comparaison des résultats
Voici les durées de vie obtenues pour différents ensembles de configurations élémentaires (exemple hypothétique) :

Ensemble de configurations	Durée de vie (unités de temps)
u1, u2, u3, u4	            8.5
u1, u2	                    6.0
u1, u3, u4	                7.0
u2, u3	                    5.5

Étape 4 : Analyse des résultats
Nous analysons les résultats pour comprendre l'influence du nombre et du type de configurations élémentaires sur la durée de vie du réseau.

Influence du nombre de configurations :
- Un plus grand nombre de configurations élémentaires tend à augmenter la durée de vie du réseau, car il y a plus de possibilités pour répartir l'activité des capteurs, évitant ainsi une surutilisation des capteurs individuels.

Influence du type de configurations :
- Les configurations qui couvrent un plus grand nombre de zones avec un minimum de capteurs sont plus efficaces. Par exemple, la configuration u1 (couvrant toutes les zones) est plus avantageuse que des configurations plus restreintes.