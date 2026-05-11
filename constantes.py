# ================================
# Auteur  : SANGARE Arouna
# Rôle    : Base de données des gaz
# Module  : constantes.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

# Constante universelle des gaz parfaits (J·mol⁻¹·K⁻¹)
R = 8.314

# Dictionnaire des gaz avec leurs constantes de Van der Waals
# a : attractions entre molécules (Pa·m⁶·mol⁻²)
# b : volume propre des molécules (m³·mol⁻¹)
GAZ = {
    "CO2": {"nom": "Dioxyde de carbone", "formule": "CO₂",  "a": 0.3640,  "b": 4.267e-5},
    "N2":  {"nom": "Diazote",            "formule": "N₂",   "a": 0.1390,  "b": 3.913e-5},
    "CH4": {"nom": "Méthane",            "formule": "CH₄",  "a": 0.2253,  "b": 4.278e-5},
    "H2O": {"nom": "Vapeur d'eau",       "formule": "H₂O",  "a": 0.5536,  "b": 3.049e-5},
    "H2":  {"nom": "Dihydrogène",        "formule": "H₂",   "a": 0.02476, "b": 2.661e-5},
    "O2":  {"nom": "Dioxygène",          "formule": "O₂",   "a": 0.1382,  "b": 3.186e-5},
    "He":  {"nom": "Hélium",             "formule": "He",   "a": 0.003457,"b": 2.370e-5},
    "NH3": {"nom": "Ammoniac",           "formule": "NH₃",  "a": 0.4225,  "b": 3.707e-5},
    "SO2": {"nom": "Dioxyde de soufre",  "formule": "SO₂",  "a": 0.6803,  "b": 5.636e-5},
    "Cl2": {"nom": "Dichlore",           "formule": "Cl₂",  "a": 0.6579,  "b": 5.622e-5},
    "Ar":  {"nom": "Argon",              "formule": "Ar",   "a": 0.1363,  "b": 3.219e-5},
    "Ne":  {"nom": "Néon",               "formule": "Ne",   "a": 0.02135, "b": 1.709e-5},
}

def lister_gaz():
    """Affiche la liste de tous les gaz disponibles."""
    print("\n  Gaz disponibles :")
    print(f"  {'Code':<8} {'Formule':<8} {'Nom complet'}")
    print("  " + "-" * 40)
    for code, infos in GAZ.items():
        print(f"  {code:<8} {infos['formule']:<8} {infos['nom']}")
    print()