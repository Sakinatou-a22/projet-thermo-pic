# Module d'affichage du tableau comparatif
from tabulate import tabulate

def afficher_resultats(gaz, formule, T, P, n, resultats):
    
    donnees = [
        ["Volume (m³)", f"{resultats['V_parfait']:.6e}", f"{resultats['V_vdw']:.6e}"],
        ["Volume (L)",  f"{resultats['V_parfait']*1000:.4f}", f"{resultats['V_vdw']*1000:.4f}"],
        ["Écart absolu (m³)", "—", f"{resultats['ecart_absolu']:.6e}"],
        ["Écart relatif (%)", "—", f"{resultats['ecart_relatif']:.4f} %"],
    ]

    entetes = ["Grandeur", "Gaz Parfait", "Van der Waals"]

    print("\n" + "=" * 60)
    print(f"  Gaz : {gaz} ({formule})")
    print(f"  T = {T} K  |  P = {P} Pa  |  n = {n} mol")
    print("=" * 60)
    print(tabulate(donnees, headers=entetes, tablefmt="fancy_grid"))
    print()