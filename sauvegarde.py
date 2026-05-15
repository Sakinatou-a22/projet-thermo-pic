# ================================
# Auteur  : CONDE Abdoulaye
# Rôle    : Export des résultats en CSV
# Module  : sauvegarde.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

import csv
from datetime import datetime

def exporter_csv(gaz, formule, T, P, n, resultats):
    """
    Exporte les résultats dans un fichier CSV.
    """
    nom_fichier = f"resultats_{gaz}_{int(T)}K.csv"

    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        writer.writerow(["Modélisation Thermodynamique — PIC"])
        writer.writerow(["Université Hassan 1er de Settat"])
        writer.writerow(["Date", datetime.now().strftime("%d/%m/%Y %H:%M")])
        writer.writerow([])
        writer.writerow(["Gaz", gaz, formule])
        writer.writerow(["Température (K)", T])
        writer.writerow(["Pression (Pa)", P])
        writer.writerow(["Quantité (mol)", n])
        writer.writerow([])
        writer.writerow(["Grandeur", "Gaz Parfait", "Van der Waals"])
        writer.writerow(["Volume (L)", 
                         round(resultats["V_parfait"]*1000, 4),
                         round(resultats["V_vdw"]*1000, 4)])
        writer.writerow(["Écart absolu (L)", "",
                         round(resultats["ecart_absolu"]*1000, 6)])
        writer.writerow(["Écart relatif (%)", "",
                         round(resultats["ecart_relatif"], 4)])

    print(f"  Résultats exportés : {nom_fichier}")