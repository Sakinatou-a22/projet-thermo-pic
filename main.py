# Programme principal
from constantes import GAZ, lister_gaz
from gaz_parfait import volume_gaz_parfait
from van_der_waals import volume_vdw
from graphique import tracer_graphique

# Affichage de bienvenue
print("=" * 50)
print("   MODÉLISATION THERMODYNAMIQUE")
print("   Gaz Parfait vs Van der Waals")
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

# Résultats
ecart = abs(V_parfait - V_reel) / V_reel * 100

print("\n" + "=" * 50)
print("  RÉSULTATS")
print("=" * 50)
print(f"  Gaz           : {gaz['nom']} ({gaz['formule']})")
print(f"  Gaz parfait   : {V_parfait*1000:.4f} L")
print(f"  Van der Waals : {V_reel*1000:.4f} L")
print(f"  Écart         : {ecart:.4f} %")
print("=" * 50)

# Graphique
tracer_graphique(P, T, n, gaz["a"], gaz["b"], gaz["nom"])