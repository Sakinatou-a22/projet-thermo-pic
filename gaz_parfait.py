# Calcul selon le modèle du gaz parfait
# Loi : PV = nRT

from constantes import R

def volume_gaz_parfait(P, T, n):
    """Calcule le volume V = nRT/P"""
    V = (n * R * T) / P
    return V