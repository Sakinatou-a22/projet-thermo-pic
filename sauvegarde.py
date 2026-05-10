# Module d'export des résultats en CSV
import csv
from datetime import datetime

def exporter_csv(gaz, formule, T, P, n, resultats):
    
    nom_fichier = f"resultats_{gaz}_{int(T)}K.csv"
    
    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        
        writer.writerow(["Modélisation Thermodynamique — PIC"])
        writer.writerow(["Date", datetime.now().strftime("%d/%m/%Y %H:%M")])
        writer.writerow([])
        writer.writerow(["Gaz", gaz, formule])
        writer.writerow(["Température (K)", T])
        writer.writerow(["Pression (Pa)", P])
        writer.writerow(["Quantité (mol)", n])
        writer.writerow([])
        writer.writerow(["Grandeur", "Gaz Parfait", "Van der Waals"])
        writer.writerow(["Volume (m³)", resultats["V_parfait"], resultats["V_vdw"]])
        writer.writerow(["Volume (L)", resultats["V_parfait"]*1000, resultats["V_vdw"]*1000])
        writer.writerow(["Écart absolu (m³)", "", resultats["ecart_absolu"]])
        writer.writerow(["Écart relatif (%)", "", resultats["ecart_relatif"]])
    
    print(f"  Résultats sauvegardés : {nom_fichier}")