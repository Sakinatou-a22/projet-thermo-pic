# Génération du rapport scientifique en PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm

def generer_rapport():
    doc = SimpleDocTemplate("rapport_thermodynamique.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    contenu = []

    # Style titre principal
    titre_style = ParagraphStyle(
        "titre", fontSize=18, fontName="Helvetica-Bold",
        alignment=1, spaceAfter=10, textColor=colors.HexColor("#1a237e"))

    # Style sous-titre
    sous_titre_style = ParagraphStyle(
        "sous_titre", fontSize=13, fontName="Helvetica",
        alignment=1, spaceAfter=20, textColor=colors.grey)

    # Style section
    section_style = ParagraphStyle(
        "section", fontSize=13, fontName="Helvetica-Bold",
        spaceBefore=15, spaceAfter=8, textColor=colors.HexColor("#1565c0"))

    # Style texte normal
    texte_style = ParagraphStyle(
        "texte", fontSize=11, fontName="Helvetica",
        spaceAfter=8, leading=16)

    # === PAGE DE GARDE ===
    contenu.append(Spacer(1, 2*cm))
    contenu.append(Paragraph("UNIVERSITÉ HASSAN 1er DE SETTAT", titre_style))
    contenu.append(Paragraph("Filière : Procédé et Ingénierie Chimique (PIC)", sous_titre_style))
    contenu.append(Spacer(1, 1*cm))
    contenu.append(Paragraph("RAPPORT DE PROJET", titre_style))
    contenu.append(Spacer(1, 0.5*cm))
    contenu.append(Paragraph(
        "Modélisation Thermodynamique : Étude comparative entre<br/>"
        "le modèle du gaz parfait et le modèle de Van der Waals",
        titre_style))
    contenu.append(Spacer(1, 2*cm))

    # Tableau équipe
    data_equipe = [
        ["Ingénieur", "Nom", "Rôle"],
        ["1", "TIENDREBEOGO Sakinatou", "Chef de projet — VdW & comparaison"],
        ["2", "SANGARE Arouna", "Module saisie & gaz parfait"],
        ["3", "CONDE Abdoulaye", "Affichage, graphique & sauvegarde"],
    ]
    tableau_equipe = Table(data_equipe, colWidths=[2*cm, 7*cm, 8*cm])
    tableau_equipe.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("PADDING",    (0,0), (-1,-1), 8),
    ]))
    contenu.append(tableau_equipe)
    contenu.append(Spacer(1, 1*cm))
    contenu.append(Paragraph("Durée du projet : 5 semaines", sous_titre_style))

    # === 1. INTRODUCTION ===
    contenu.append(Paragraph("1. Introduction", section_style))
    contenu.append(Paragraph(
        "Dans le cadre du cours de thermodynamique de la filière Procédé et Ingénierie "
        "Chimique (PIC), ce projet consiste à comparer deux modèles fondamentaux du "
        "comportement des gaz : le modèle du gaz parfait et le modèle de Van der Waals. "
        "L'objectif est de développer une application Python permettant de calculer, "
        "comparer et visualiser les propriétés thermodynamiques des gaz réels.",
        texte_style))

    # === 2. THÉORIE ===
    contenu.append(Paragraph("2. Théorie des deux modèles", section_style))

    contenu.append(Paragraph("2.1 Modèle du gaz parfait", sous_titre_style))
    contenu.append(Paragraph(
        "La loi des gaz parfaits est définie par l'équation PV = nRT, où P est la pression "
        "(Pa), V le volume (m³), n la quantité de matière (mol), R = 8,314 J/(mol·K) la "
        "constante universelle des gaz, et T la température (K). Ce modèle suppose que "
        "les molécules n'ont pas de volume propre et qu'il n'existe aucune interaction "
        "entre elles.",
        texte_style))

    contenu.append(Paragraph("2.2 Modèle de Van der Waals", sous_titre_style))
    contenu.append(Paragraph(
        "L'équation de Van der Waals corrige le modèle du gaz parfait en tenant compte "
        "de deux phénomènes réels : (P + an²/V²)(V - nb) = nRT. "
        "La constante a représente les forces attractives entre molécules, "
        "et b représente le volume propre des molécules.",
        texte_style))

    # Tableau constantes
    contenu.append(Paragraph("Constantes de Van der Waals :", texte_style))
    data_cst = [
        ["Gaz", "Formule", "a (Pa·m⁶/mol²)", "b (m³/mol)"],
        ["Dioxyde de carbone", "CO₂", "0.3640", "4.267 × 10⁻⁵"],
        ["Diazote",            "N₂",  "0.1390", "3.913 × 10⁻⁵"],
        ["Méthane",            "CH₄", "0.2253", "4.278 × 10⁻⁵"],
        ["Vapeur d'eau",       "H₂O", "0.5536", "3.049 × 10⁻⁵"],
    ]
    tableau_cst = Table(data_cst, colWidths=[5*cm, 3*cm, 4.5*cm, 4.5*cm])
    tableau_cst.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("PADDING",    (0,0), (-1,-1), 6),
    ]))
    contenu.append(tableau_cst)

    # === 3. ARCHITECTURE ===
    contenu.append(Paragraph("3. Architecture de l'application", section_style))
    contenu.append(Paragraph(
        "L'application est organisée en 8 modules indépendants :",
        texte_style))
    data_arch = [
        ["Fichier", "Rôle"],
        ["main.py",          "Programme principal — point d'entrée"],
        ["interface.py",     "Interface graphique Tkinter"],
        ["constantes.py",    "Base de données des gaz"],
        ["gaz_parfait.py",   "Calcul selon PV = nRT"],
        ["van_der_waals.py", "Calcul selon l'équation de Van der Waals"],
        ["comparaison.py",   "Calcul des écarts entre les deux modèles"],
        ["affichage.py",     "Affichage du tableau comparatif"],
        ["graphique.py",     "Tracé de la courbe P–V"],
        ["sauvegarde.py",    "Export des résultats en CSV"],
    ]
    tableau_arch = Table(data_arch, colWidths=[5*cm, 12*cm])
    tableau_arch.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("ALIGN",      (0,0), (0,-1), "CENTER"),
        ("PADDING",    (0,0), (-1,-1), 6),
    ]))
    contenu.append(tableau_arch)

    # === 4. RÉSULTATS ===
    contenu.append(Paragraph("4. Résultats et analyse", section_style))
    contenu.append(Paragraph(
        "Pour le CO₂ à T = 300 K et P = 101 325 Pa (1 atm) avec n = 1 mol :",
        texte_style))
    data_res = [
        ["Grandeur",        "Gaz parfait",    "Van der Waals"],
        ["Volume (L)",      "24.6158 L",      "24.5122 L"],
        ["Écart absolu",    "—",              "0.1036 L"],
        ["Écart relatif",   "—",              "0.4228 %"],
    ]
    tableau_res = Table(data_res, colWidths=[5*cm, 6*cm, 6*cm])
    tableau_res.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("PADDING",    (0,0), (-1,-1), 8),
    ]))
    contenu.append(tableau_res)
    contenu.append(Spacer(1, 0.5*cm))
    contenu.append(Paragraph(
        "L'écart de 0.42% à pression atmosphérique montre que les deux modèles sont "
        "proches dans ces conditions. Cet écart augmente significativement à haute "
        "pression, où les interactions moléculaires deviennent importantes.",
        texte_style))

    # === 5. CONCLUSION ===
    contenu.append(Paragraph("5. Conclusion", section_style))
    contenu.append(Paragraph(
        "Ce projet nous a permis de développer une application Python complète de "
        "modélisation thermodynamique. Nous avons implémenté et comparé deux modèles "
        "fondamentaux : le gaz parfait et Van der Waals. Les résultats montrent que "
        "le modèle de Van der Waals est plus précis pour les gaz réels, surtout à "
        "haute pression et basse température. L'application dispose d'une interface "
        "graphique, d'un graphique P–V et d'un export CSV des résultats.",
        texte_style))

    doc.build(contenu)
    print("Rapport généré : rapport_thermodynamique.pdf")

generer_rapport()