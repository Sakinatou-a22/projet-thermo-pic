# ================================
# Auteur  : SANGARE Arouna
# Rôle    : Calcul selon le modèle du gaz parfait
# Module  : gaz_parfait.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

from constantes import R


def volume_gaz_parfait(P, T, n):
    """
    Calcule le volume d'un gaz parfait.
    Loi : PV = nRT

    Paramètres
    ----------
    P : float — Pression en Pa
    T : float — Température en K
    n : float — Quantité de matière en mol

    Retourne
    --------
    V : float — Volume en m³
    """
    V = (n * R * T) / P
    return V


def courbe_PV_parfait(T, n, V_min, V_max, nb_points=200):
    """
    Génère les points de la courbe P-V pour le gaz parfait.

    Retourne
    --------
    volumes   : list — Liste des volumes en m³
    pressions : list — Liste des pressions en Pa
    """
    import numpy as np
    volumes = np.linspace(V_min, V_max, nb_points)
    pressions = [(n * R * T) / V for V in volumes]
    return list(volumes), pressions