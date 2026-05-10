# Module de comparaison des deux modèles

def comparer(V_parfait, V_vdw):
    ecart_absolu  = abs(V_parfait - V_vdw)
    ecart_relatif = (ecart_absolu / V_vdw) * 100

    return {
        "V_parfait":     V_parfait,
        "V_vdw":         V_vdw,
        "ecart_absolu":  ecart_absolu,
        "ecart_relatif": ecart_relatif,
    }