# Constante universelle des gaz parfaits
R = 8.314

# Base de données des gaz
GAZ = {
    "CO2": {"nom": "Dioxyde de carbone", "formule": "CO₂", "a": 0.3640, "b": 4.267e-5},
    "N2":  {"nom": "Diazote",            "formule": "N₂",  "a": 0.1390, "b": 3.913e-5},
    "CH4": {"nom": "Méthane",            "formule": "CH₄", "a": 0.2253, "b": 4.278e-5},
    "H2O": {"nom": "Vapeur d'eau",       "formule": "H₂O", "a": 0.5536, "b": 3.049e-5},
}

def lister_gaz():
    print("\n  Gaz disponibles :")
    print(f"  {'Code':<8} {'Formule':<8} {'Nom'}")
    print("  " + "-" * 35)
    for code, infos in GAZ.items():
        print(f"  {code:<8} {infos['formule']:<8} {infos['nom']}")
    print()