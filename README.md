# Projet Thermodynamique — PIC
## Université Hassan 1er de Settat

### Description
Application Python de modélisation thermodynamique comparant le modèle du gaz parfait et le modèle de Van der Waals.

---

### Équipe

| Ingénieur | Nom | Rôle |
|-----------|-----|------|
| 1 | TIENDREBEOGO Sakinatou | Chef de projet — Coordination, calculs Van der Waals et comparaison |
| 2 | SANGARE Arouna | Module saisie et gaz parfait |
| 3 | CONDE Abdoulaye | Affichage, graphique et sauvegarde |

---

### Architecture du projet

main.py          - Programme principal
constantes.py    - Base de données des gaz
gaz_parfait.py   - Modèle gaz parfait (PV = nRT)
van_der_waals.py - Modèle Van der Waals
comparaison.py   - Calcul des écarts
affichage.py     - Tableau comparatif
graphique.py     - Courbe P-V matplotlib
sauvegarde.py    - Export CSV

---

### Installation
pip install matplotlib tabulate scipy
python main.py

---

### Résultats attendus
- Tableau comparatif des deux modèles
- Courbe P-V superposant les deux modèles
- Export CSV des résultats