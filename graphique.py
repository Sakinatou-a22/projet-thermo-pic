# ================================
# Auteur  : CONDE Abdoulaye
# Rôle    : Tracé de la courbe P-V
# Module  : graphique.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

import numpy as np
import matplotlib.pyplot as plt
from gaz_parfait import volume_gaz_parfait
from van_der_waals import volume_vdw

def tracer_graphique(P, T, n, a, b, nom_gaz, chemin_png=None):
    """
    Trace la courbe P-V pour les deux modèles superposés.
    """
    pressions = np.linspace(P * 0.1, P * 5, 200)

    V_gp  = [volume_gaz_parfait(p, T, n) * 1000 for p in pressions]
    V_vdw = [volume_vdw(p, T, n, a, b) * 1000 for p in pressions]

    plt.figure(figsize=(10, 6))
    plt.plot(V_gp,  pressions/1e5, color="blue", linewidth=2,
             linestyle="--", label="Gaz parfait (PV = nRT)")
    plt.plot(V_vdw, pressions/1e5, color="red",  linewidth=2,
             label="Van der Waals")

    plt.title(f"Courbe P–V — {nom_gaz} — T = {T} K")
    plt.xlabel("Volume V (L)")
    plt.ylabel("Pression P (bar)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if chemin_png:
        plt.savefig(chemin_png, dpi=150)
        print(f"  Graphique sauvegardé : {chemin_png}")

    plt.show()