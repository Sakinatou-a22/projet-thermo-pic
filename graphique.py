# Module graphique — Courbe P-V
import numpy as np
import matplotlib.pyplot as plt
from gaz_parfait import volume_gaz_parfait
from van_der_waals import volume_vdw

def tracer_graphique(P, T, n, a, b, nom_gaz):
    
    # Plage de pressions
    pressions = np.linspace(P * 0.1, P * 5, 200)
    
    # Calcul des volumes pour chaque pression
    V_parfait = [volume_gaz_parfait(p, T, n) * 1000 for p in pressions]
    V_reel    = [volume_vdw(p, T, n, a, b) * 1000 for p in pressions]

    # Tracé
    plt.figure(figsize=(10, 6))
    plt.plot(V_parfait, pressions/1e5, color="blue", 
             linewidth=2, linestyle="--", label="Gaz parfait")
    plt.plot(V_reel, pressions/1e5, color="red",  
             linewidth=2, label="Van der Waals")

    plt.title(f"Courbe P–V — {nom_gaz} — T = {T} K")
    plt.xlabel("Volume V (L)")
    plt.ylabel("Pression P (bar)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("graphique.png", dpi=150)
    plt.show()
    print("  Graphique sauvegardé : graphique.png")