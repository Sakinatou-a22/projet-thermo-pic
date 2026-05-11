# ================================
# Auteur  : SANGARE Arouna
# Rôle    : Programme principal
# Module  : main.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

from constantes import GAZ, lister_gaz
from gaz_parfait import volume_gaz_parfait
from van_der_waals import volume_vdw
from comparaison import comparer
from affichage import afficher_resultats
from sauvegarde import exporter_csv
from graphique import tracer_graphique

# Affichage de bienvenue
print("=" * 50)
print("   MODÉLISATION THERMODYNAMIQUE")
print("   Gaz Parfait vs Van der Waals")
print("   Université Hassan 1er de Settat")
print("=" * 50)

# Choix du gaz
lister_gaz()
code = input("  Entrez le code du gaz : ").strip().upper()
gaz = GAZ[code]

# Saisie des paramètres
T = float(input("  Température T (en K) : "))
P = float(input("  Pression P (en Pa)   : "))
n = float(input("  Quantité n (en mol)  : "))

# Calculs
V_parfait = volume_gaz_parfait(P, T, n)
V_reel    = volume_vdw(P, T, n, gaz["a"], gaz["b"])

# Comparaison
resultats = comparer(V_parfait, V_reel)

# Affichage tableau
afficher_resultats(gaz["nom"], gaz["formule"], T, P, n, resultats)

# Sauvegarde CSV
exporter_csv(gaz["nom"], gaz["formule"], T, P, n, resultats)

# Graphique
tracer_graphique(P, T, n, gaz["a"], gaz["b"], gaz["nom"])