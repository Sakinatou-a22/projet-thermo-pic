# Calcul selon le modèle de Van der Waals
# Équation : (P + a·n²/V²)(V − n·b) = nRT

from scipy.optimize import brentq
from constantes import R

def volume_vdw(P, T, n, a, b):
    """Calcule le volume selon Van der Waals (résolution numérique)"""
    
    def equation(V):
        return (P + a * n**2 / V**2) * (V - n * b) - n * R * T

    V_min = n * b * 1.001
    V_max = (n * R * T / P) * 10

    V_solution = brentq(equation, V_min, V_max)
    return V_solution
