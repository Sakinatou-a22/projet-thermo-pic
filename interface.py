# Interface graphique — Modélisation Thermodynamique
import tkinter as tk
from tkinter import ttk, messagebox
from constantes import GAZ
from gaz_parfait import volume_gaz_parfait
from van_der_waals import volume_vdw
from comparaison import comparer
from graphique import tracer_graphique

# === Fenêtre principale ===
fenetre = tk.Tk()
fenetre.title("Modélisation Thermodynamique — PIC")
fenetre.geometry("500x600")
fenetre.configure(bg="#1e1e2e")

# === Titre ===
titre = tk.Label(fenetre, 
    text="Modélisation Thermodynamique",
    font=("Arial", 16, "bold"),
    bg="#1e1e2e", fg="white")
titre.pack(pady=15)

sous_titre = tk.Label(fenetre,
    text="Gaz Parfait vs Van der Waals",
    font=("Arial", 11),
    bg="#1e1e2e", fg="#aaaaaa")
sous_titre.pack()

# === Cadre de saisie ===
cadre = tk.Frame(fenetre, bg="#2e2e3e", padx=20, pady=20)
cadre.pack(pady=20, padx=30, fill="x")

# Choix du gaz
tk.Label(cadre, text="Gaz :", bg="#2e2e3e", fg="white",
         font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
choix_gaz = ttk.Combobox(cadre, values=list(GAZ.keys()), width=20)
choix_gaz.set("CO2")
choix_gaz.grid(row=0, column=1, pady=8, padx=10)

# Température
tk.Label(cadre, text="Température (K) :", bg="#2e2e3e", fg="white",
         font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
champ_T = tk.Entry(cadre, width=22)
champ_T.insert(0, "300")
champ_T.grid(row=1, column=1, pady=8, padx=10)

# Pression
tk.Label(cadre, text="Pression (Pa) :", bg="#2e2e3e", fg="white",
         font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=8)
champ_P = tk.Entry(cadre, width=22)
champ_P.insert(0, "101325")
champ_P.grid(row=2, column=1, pady=8, padx=10)

# Quantité
tk.Label(cadre, text="Quantité (mol) :", bg="#2e2e3e", fg="white",
         font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=8)
champ_n = tk.Entry(cadre, width=22)
champ_n.insert(0, "1.0")
champ_n.grid(row=3, column=1, pady=8, padx=10)

# === Zone résultats ===
zone_resultats = tk.Text(fenetre, height=10, width=55,
                          bg="#2e2e3e", fg="#00ff99",
                          font=("Courier", 10), state="disabled")
zone_resultats.pack(pady=10, padx=30)

# === Fonction calcul ===
def calculer():
    try:
        code = choix_gaz.get()
        T = float(champ_T.get())
        P = float(champ_P.get())
        n = float(champ_n.get())
        gaz = GAZ[code]

        V_gp  = volume_gaz_parfait(P, T, n)
        V_vdw = volume_vdw(P, T, n, gaz["a"], gaz["b"])
        res   = comparer(V_gp, V_vdw)

        texte = f"""
  Gaz : {gaz['nom']} ({gaz['formule']})
  T = {T} K  |  P = {P} Pa  |  n = {n} mol
  {'─'*40}
  Gaz parfait   : {V_gp*1000:.4f} L
  Van der Waals : {V_vdw*1000:.4f} L
  Écart absolu  : {res['ecart_absolu']*1000:.6f} L
  Écart relatif : {res['ecart_relatif']:.4f} %
        """

        zone_resultats.config(state="normal")
        zone_resultats.delete("1.0", tk.END)
        zone_resultats.insert(tk.END, texte)
        zone_resultats.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def afficher_graphique():
    try:
        code = choix_gaz.get()
        T = float(champ_T.get())
        P = float(champ_P.get())
        n = float(champ_n.get())
        gaz = GAZ[code]
        tracer_graphique(P, T, n, gaz["a"], gaz["b"], gaz["nom"])
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# === Boutons ===
cadre_boutons = tk.Frame(fenetre, bg="#1e1e2e")
cadre_boutons.pack(pady=10)

btn_calculer = tk.Button(cadre_boutons,
    text="Calculer",
    command=calculer,
    bg="#4CAF50", fg="white",
    font=("Arial", 12, "bold"),
    padx=20, pady=8, cursor="hand2")
btn_calculer.grid(row=0, column=0, padx=10)

btn_graphique = tk.Button(cadre_boutons,
    text="Voir Graphique",
    command=afficher_graphique,
    bg="#2196F3", fg="white",
    font=("Arial", 12, "bold"),
    padx=20, pady=8, cursor="hand2")
btn_graphique.grid(row=0, column=1, padx=10)

fenetre.mainloop()