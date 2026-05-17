from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy.integrate import quad
import io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

R = 8.314  # J/(mol·K)

# ─── Utility ────────────────────────────────────────────────────────────────

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()

STYLE = dict(facecolor='#0f1117', edgecolor='none')
AXSTYLE = dict(facecolor='#0f1117', labelcolor='#c9d1d9', titlecolor='#58a6ff')
GRID = dict(color='#21262d', linestyle='--', linewidth=0.5)

def styled_fig(figsize=(9,5)):
    fig, ax = plt.subplots(figsize=figsize, **STYLE)
    ax.set_facecolor('#0f1117')
    ax.tick_params(colors='#8b949e')
    for spine in ax.spines.values():
        spine.set_edgecolor('#21262d')
    ax.grid(**GRID)
    return fig, ax

# ═══════════════════════════════════════════════════════════════════════════
# EXERCICE 1.1 – Pression de bulle benzène/toluène (photo)
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/ex11', methods=['POST'])
def ex11():
    d = request.json
    x1 = float(d.get('x1', 0.40))      # fraction molaire benzène liquide
    P1sat = float(d.get('P1sat', 101.3))  # kPa
    P2sat = float(d.get('P2sat', 40.0))   # kPa
    x2 = 1.0 - x1

    # Loi de Raoult : P_bulle = x1*P1sat + x2*P2sat
    P_bulle = x1 * P1sat + x2 * P2sat

    # Fractions molaires vapeur : yi = xi*Pisat / P_bulle
    y1 = x1 * P1sat / P_bulle
    y2 = x2 * P2sat / P_bulle
    check = y1 + y2

    # Graphe x-y et diagramme de bulle/rosée
    x_range = np.linspace(0, 1, 200)
    P_range = x_range * P1sat + (1 - x_range) * P2sat   # courbe de bulle
    y1_range = x_range * P1sat / P_range                  # courbe de rosée (inverser)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), **STYLE)
    for ax in axes:
        ax.set_facecolor('#0f1117')
        ax.tick_params(colors='#8b949e')
        for sp in ax.spines.values(): sp.set_edgecolor('#21262d')
        ax.grid(**GRID)

    # Diagramme P-x-y
    ax1 = axes[0]
    x_for_y = np.linspace(0, 1, 200)
    P_bub = x_for_y * P1sat + (1 - x_for_y) * P2sat
    y1_dew_x = x_for_y * P1sat / P_bub   # y1 en fonction de x1

    ax1.plot(x_for_y, P_bub, color='#58a6ff', lw=2, label='Courbe de bulle (liquide)')
    ax1.plot(y1_dew_x, P_bub, color='#f78166', lw=2, label='Courbe de rosée (vapeur)')
    ax1.axvline(x1, color='#3fb950', ls='--', alpha=0.7)
    ax1.axhline(P_bulle, color='#d2a8ff', ls='--', alpha=0.7)
    ax1.scatter([x1], [P_bulle], color='#ffa657', s=80, zorder=5, label=f'Point opératoire (x₁={x1})')
    ax1.set_xlabel('Fraction molaire benzène', color='#c9d1d9')
    ax1.set_ylabel('Pression (kPa)', color='#c9d1d9')
    ax1.set_title('Diagramme P-x-y à T=80°C', color='#58a6ff')
    ax1.legend(fontsize=8, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')

    # Diagramme y-x (McCabe-Thiele)
    ax2 = axes[1]
    ax2.plot(x_for_y, y1_dew_x, color='#58a6ff', lw=2, label='Équilibre y₁(x₁)')
    ax2.plot([0,1],[0,1], color='#8b949e', ls='--', lw=1, label='Diagonale')
    ax2.scatter([x1], [y1], color='#ffa657', s=80, zorder=5, label=f'(x₁={x1:.2f}, y₁={y1:.3f})')
    ax2.set_xlabel('x₁ (liquide, benzène)', color='#c9d1d9')
    ax2.set_ylabel('y₁ (vapeur, benzène)', color='#c9d1d9')
    ax2.set_title('Diagramme y-x (McCabe-Thiele)', color='#58a6ff')
    ax2.legend(fontsize=8, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')

    fig.patch.set_facecolor('#0f1117')
    img = fig_to_b64(fig)

    return jsonify({
        'P_bulle': round(P_bulle, 3),
        'y1': round(y1, 4),
        'y2': round(y2, 4),
        'check_sum_yi': round(check, 6),
        'plot': img
    })

# ═══════════════════════════════════════════════════════════════════════════
# EXERCICE 1 – Équation de van der Waals
# ═══════════════════════════════════════════════════════════════════════════

VDW_DATA = {
    'CO2':  dict(a=0.3640, b=4.267e-5, Tc=304.2, Pc=73.8e5),
    'CH4':  dict(a=0.2283, b=4.278e-5, Tc=190.6, Pc=46.1e5),
    'H2O':  dict(a=0.5537, b=3.049e-5, Tc=647.1, Pc=220.6e5),
    'N2':   dict(a=0.1370, b=3.870e-5, Tc=126.2, Pc=34.0e5),
    'C3H8': dict(a=0.9385, b=9.049e-5, Tc=369.8, Pc=42.5e5),
}

def pression_vdw(T, Vm, a, b):
    return R * T / (Vm - b) - a / Vm**2

def resoudre_vdw(T, P, a, b):
    c2 = -(b + R*T/P)
    c1 = a/P
    c0 = -a*b/P
    roots = np.roots([1, c2, c1, c0])
    real_roots = roots[np.isreal(roots)].real
    return sorted(real_roots[real_roots > b])

@app.route('/ex1_a1', methods=['POST'])
def ex1_a1():
    d = request.json
    comp = d.get('compound', 'CO2')
    T = float(d.get('T', 300))
    P = float(d.get('P', 100)) * 1e5
    params = VDW_DATA[comp]
    a, b = params['a'], params['b']

    roots = resoudre_vdw(T, P, a, b)
    Vm_gp = R * T / P

    results = []
    for i, Vm in enumerate(roots):
        err_rel = abs(Vm - Vm_gp) / Vm_gp * 100
        results.append({
            'label': ['Liquide', 'Intermédiaire', 'Gaz'][i] if len(roots) == 3 else f'Racine {i+1}',
            'Vm_vdw_cm3': round(Vm * 1e6, 2),
            'err_rel_pct': round(err_rel, 2)
        })

    return jsonify({
        'Vm_gp_cm3': round(Vm_gp * 1e6, 2),
        'roots': results,
        'n_roots': len(roots)
    })

@app.route('/ex1_b1', methods=['POST'])
def ex1_b1():
    d = request.json
    comp = d.get('compound', 'CO2')
    params = VDW_DATA[comp]
    a, b, Tc, Pc = params['a'], params['b'], params['Tc'], params['Pc']

    temperatures = [0.82*Tc, 0.92*Tc, Tc, 1.08*Tc, 1.32*Tc]
    colors = ['#58a6ff','#f78166','#3fb950','#ffa657','#d2a8ff']
    labels = [f'T={T:.0f} K (Tr={T/Tc:.2f})' for T in temperatures]

    Vm_arr = np.linspace(b * 1.05, 5e-4, 3000)
    fig, ax = styled_fig((10, 5))

    for T, color, lbl in zip(temperatures, colors, labels):
        P_arr = pression_vdw(T, Vm_arr, a, b)
        P_plot = np.where(np.abs(P_arr) > 3e7, np.nan, P_arr)
        ax.plot(Vm_arr * 1e3, P_plot / 1e5, color=color, lw=2, label=lbl)

    ax.axhline(Pc/1e5, color='#8b949e', ls=':', lw=1.5, label=f'Pc = {Pc/1e5:.1f} bar')
    ax.set_xlabel('Volume molaire Vm (L/mol)', color='#c9d1d9')
    ax.set_ylabel('Pression P (bar)', color='#c9d1d9')
    ax.set_title(f'Isothermes de van der Waals – {comp}', color='#58a6ff', fontsize=13)
    ax.legend(fontsize=8, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')
    ax.set_xlim(0, 0.5); ax.set_ylim(-20, 500)
    fig.patch.set_facecolor('#0f1117')

    # Point critique
    Vc_m = 3*b
    ax.scatter([Vc_m*1e3],[Pc/1e5], color='white', s=60, zorder=6, label='Point critique')

    return jsonify({'plot': fig_to_b64(fig), 'compound': comp, 'Tc': Tc, 'Pc': round(Pc/1e5,1)})

@app.route('/ex1_b3', methods=['POST'])
def ex1_b3():
    d = request.json
    comp = d.get('compound', 'CO2')
    T = float(d.get('T', 280))
    params = VDW_DATA[comp]
    a, b, Tc = params['a'], params['b'], params['Tc']

    P_range = np.linspace(5e5, 80e5, 500)
    roots_list = [resoudre_vdw(T, P, a, b) for P in P_range]
    three_roots = [(P, r) for P, r in zip(P_range, roots_list) if len(r) == 3]

    result = {}
    if three_roots:
        P_ex = three_roots[len(three_roots)//2][0]
        roots_ex = resoudre_vdw(T, P_ex, a, b)
        result = {
            'T': T, 'P_bar': round(P_ex/1e5, 2),
            'Vm_liq': round(roots_ex[0]*1e6, 2),
            'Vm_mid': round(roots_ex[1]*1e6, 2) if len(roots_ex)>2 else None,
            'Vm_gas': round(roots_ex[-1]*1e6, 2),
        }
    return jsonify(result)

# ═══════════════════════════════════════════════════════════════════════════
# EXERCICE 2 – Corrélation de Pitzer
# ═══════════════════════════════════════════════════════════════════════════

PITZER_DATA = {
    'C3H8': dict(Tc=369.8, Pc=42.5, omega=0.152),
    'CH4':  dict(Tc=190.6, Pc=46.1, omega=0.012),
    'C5H12':dict(Tc=469.7, Pc=33.7, omega=0.252),
    'CO2':  dict(Tc=304.2, Pc=73.8, omega=0.225),
    'N2':   dict(Tc=126.2, Pc=34.0, omega=0.039),
}

def calc_Z_pitzer(T, P_bar, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P_bar / Pc
    B0 = 0.083 - 0.422 / Tr**1.6
    B1 = 0.139 - 0.172 / Tr**4.2
    return 1 + (B0 + omega * B1) * Pr / Tr

@app.route('/ex2_calc', methods=['POST'])
def ex2_calc():
    d = request.json
    comp = d.get('compound', 'C3H8')
    T = float(d.get('T', 400))
    P = float(d.get('P', 20))
    params = PITZER_DATA[comp]
    Tc, Pc, omega = params['Tc'], params['Pc'], params['omega']

    Z = calc_Z_pitzer(T, P, Tc, Pc, omega)
    Vm_vdw = Z * R * T / (P * 1e5) * 1e6   # cm³/mol
    Vm_gp  = R * T / (P * 1e5) * 1e6
    Tr = T/Tc; Pr = P/Pc

    # Plot Z(Pr) pour plusieurs Tr
    Tr_vals = [1.0, 1.2, 1.5, 2.0]
    colors_p = ['#f78166','#58a6ff','#3fb950','#ffa657']
    Pr_arr = np.linspace(0.01, 10, 300)
    fig, ax = styled_fig((9, 5))
    for Tr_i, c in zip(Tr_vals, colors_p):
        Z_arr = [calc_Z_pitzer(Tr_i*Tc, Pr_j*Pc, Tc, Pc, omega) for Pr_j in Pr_arr]
        ax.plot(Pr_arr, Z_arr, color=c, lw=2, label=f'Tr = {Tr_i}')
    ax.axhline(1, color='#8b949e', ls='--', lw=1)
    ax.scatter([Pr],[Z], color='white', s=80, zorder=5, label=f'Point ({comp})')
    ax.set_xlabel('Pression réduite Pr', color='#c9d1d9')
    ax.set_ylabel('Facteur de compressibilité Z', color='#c9d1d9')
    ax.set_title(f'Diagramme Z(Pr) – {comp} (ω={omega})', color='#58a6ff')
    ax.legend(fontsize=9, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')
    fig.patch.set_facecolor('#0f1117')

    return jsonify({
        'Z': round(Z, 4), 'Tr': round(Tr,3), 'Pr': round(Pr,3),
        'Vm_pitzer_cm3': round(Vm_vdw, 2),
        'Vm_gp_cm3': round(Vm_gp, 2),
        'err_rel_pct': round(abs(Vm_vdw-Vm_gp)/Vm_gp*100, 2),
        'plot': fig_to_b64(fig)
    })

@app.route('/ex2_compare', methods=['POST'])
def ex2_compare():
    compounds = ['C3H8','CH4','C5H12']
    names = ['Propane','Méthane','Pentane']
    Tr_target, Pr_target = 1.2, 3.0
    results = []
    for comp, name in zip(compounds, names):
        p = PITZER_DATA[comp]
        T = Tr_target * p['Tc']; P = Pr_target * p['Pc']
        Z = calc_Z_pitzer(T, P, p['Tc'], p['Pc'], p['omega'])
        results.append({'compound': name, 'omega': p['omega'], 'Z': round(Z,4),
                        'T_K': round(T,1), 'P_bar': round(P,1)})
    return jsonify({'results': results, 'Tr': Tr_target, 'Pr': Pr_target})

# ═══════════════════════════════════════════════════════════════════════════
# EXERCICE 3 – Chaleur et enthalpie (eau 20°C → 150°C)
# ═══════════════════════════════════════════════════════════════════════════

def Cp_vapeur(T):
    t = T / 1000
    return 30.09 + 6.833e-3*t + 6.793e-3*t**2 - 2.534e-3*t**3 + 0.082/t**2

@app.route('/ex3', methods=['POST'])
def ex3():
    d = request.json
    masse = float(d.get('masse', 5))      # kg
    T1_c = float(d.get('T1', 20))         # °C
    T3_c = float(d.get('T3', 150))        # °C

    M_eau = 18e-3  # kg/mol
    n = masse / M_eau

    T1 = T1_c + 273.15
    T_eb = 373.15
    T3 = T3_c + 273.15

    Cp_liq = 75.94  # J/(mol·K)
    dHvap = 40700   # J/mol

    dH1_mol = Cp_liq * (T_eb - T1)
    dH2_mol = dHvap
    dH3_mol, _ = quad(Cp_vapeur, T_eb, T3)
    dH_total_mol = dH1_mol + dH2_mol + dH3_mol

    dH1_kJ = n * dH1_mol / 1e3
    dH2_kJ = n * dH2_mol / 1e3
    dH3_kJ = n * dH3_mol / 1e3
    dH_total_kJ = n * dH_total_mol / 1e3

    # Profil enthalpique
    T_range1 = np.linspace(T1, T_eb, 100)
    T_range3 = np.linspace(T_eb, T3, 60)
    H_liq  = [n * Cp_liq * (T - T1) / 1e3 for T in T_range1]
    H_vap_base = n * (dH1_mol + dH2_mol) / 1e3
    H_vap  = [H_vap_base + n * quad(Cp_vapeur, T_eb, T)[0] / 1e3 for T in T_range3]

    fig, ax = styled_fig((10, 5))
    ax.plot(T_range1 - 273.15, H_liq, color='#58a6ff', lw=2.5, label='① Eau liquide')
    ax.axvline(100, color='#8b949e', ls=':', lw=1)
    ax.plot([100, 100], [H_liq[-1], H_vap_base], color='#f78166', lw=2.5, label='② Vaporisation')
    ax.plot(T_range3 - 273.15, H_vap, color='#3fb950', lw=2.5, label='③ Vapeur surchauffée')
    ax.set_xlabel('Température (°C)', color='#c9d1d9')
    ax.set_ylabel('Enthalpie accumulée (kJ)', color='#c9d1d9')
    ax.set_title(f'Profil enthalpique H(T) pour {masse} kg d\'eau', color='#58a6ff')
    ax.legend(fontsize=9, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')
    fig.patch.set_facecolor('#0f1117')

    return jsonify({
        'n_mol': round(n, 2),
        'dH1_kJ': round(dH1_kJ, 1),
        'dH2_kJ': round(dH2_kJ, 1),
        'dH3_kJ': round(dH3_kJ, 1),
        'dH_total_kJ': round(dH_total_kJ, 1),
        'dH1_mol': round(dH1_mol/1e3, 3),
        'dH2_mol': round(dH2_mol/1e3, 3),
        'dH3_mol': round(dH3_mol/1e3, 3),
        'plot': fig_to_b64(fig)
    })

# ═══════════════════════════════════════════════════════════════════════════
# EXERCICE 4 – Cycle de Carnot
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/ex4', methods=['POST'])
def ex4():
    d = request.json
    T1 = float(d.get('T1', 600))   # K source chaude
    T2 = float(d.get('T2', 300))   # K source froide
    VA = float(d.get('VA', 1e-3))  # m³  (1 L)
    VB_ratio = float(d.get('VB_ratio', 3))  # VB = ratio * VA
    gamma = 5/3
    n = 1.0

    eta = 1 - T2/T1
    VB = VB_ratio * VA
    # B→C adiabatique: T1*VB^(γ-1) = T2*VC^(γ-1)
    VC = VB * (T1/T2)**(1/(gamma-1))
    # D→A adiabatique: T2*VD^(γ-1) = T1*VA^(γ-1)
    VD = VA * (T1/T2)**(1/(gamma-1))

    Cv = R / (gamma - 1)

    # Travaux et chaleurs
    W_AB = -n*R*T1*np.log(VB/VA)
    Q_AB =  n*R*T1*np.log(VB/VA)
    dU_AB = 0.0

    W_BC = n*Cv*(T2-T1)
    Q_BC = 0.0
    dU_BC = n*Cv*(T2-T1)

    W_CD = -n*R*T2*np.log(VD/VC)
    Q_CD =  n*R*T2*np.log(VD/VC)
    dU_CD = 0.0

    W_DA = n*Cv*(T1-T2)
    Q_DA = 0.0
    dU_DA = n*Cv*(T1-T2)

    W_net = W_AB + W_BC + W_CD + W_DA
    Q_total = Q_AB + Q_CD
    dU_cycle = dU_AB + dU_BC + dU_CD + dU_DA
    eta_verif = -W_net / Q_AB

    # Diagramme P-V
    def P_iso(V, T): return n*R*T/V
    def P_adi(V, V0, T0): return n*R*T0/V0 * (V0/V)**gamma

    V_AB = np.linspace(VA, VB, 200)
    V_BC = np.linspace(VB, VC, 200)
    V_CD = np.linspace(VC, VD, 200)
    V_DA = np.linspace(VD, VA, 200)

    P_AB = P_iso(V_AB, T1)
    P_BC = P_adi(V_BC, VB, T1)
    P_CD = P_iso(V_CD, T2)
    P_DA = P_adi(V_DA, VD, T2)

    fig, ax = styled_fig((9, 5))
    colors_c = ['#58a6ff','#f78166','#3fb950','#ffa657']
    labels_c = ['A→B (isotherme T₁)','B→C (adiabatique)','C→D (isotherme T₂)','D→A (adiabatique)']
    for V_s, P_s, c, l in zip([V_AB,V_BC,V_CD,V_DA],[P_AB,P_BC,P_CD,P_DA],colors_c,labels_c):
        ax.plot(V_s*1e3, P_s/1e5, color=c, lw=2.5, label=l)

    # Hachures
    V_fill = np.concatenate([V_AB, V_BC, V_CD[::-1], V_DA[::-1]])
    P_fill = np.concatenate([P_AB, P_BC, P_CD[::-1], P_DA[::-1]])
    ax.fill(V_fill*1e3, P_fill/1e5, alpha=0.15, color='#58a6ff')

    for V, P, lbl in zip([VA,VB,VC,VD],[P_iso(VA,T1),P_iso(VB,T1),P_iso(VC,T2),P_iso(VD,T2)],['A','B','C','D']):
        ax.scatter([V*1e3],[P/1e5], s=60, color='white', zorder=5)
        ax.annotate(lbl, (V*1e3, P/1e5), color='white', fontsize=11,
                    textcoords='offset points', xytext=(6,6))

    ax.set_xlabel('Volume V (L)', color='#c9d1d9')
    ax.set_ylabel('Pression P (bar)', color='#c9d1d9')
    ax.set_title(f'Cycle de Carnot – T₁={T1} K, T₂={T2} K', color='#58a6ff')
    ax.legend(fontsize=8, facecolor='#161b22', edgecolor='#21262d', labelcolor='#c9d1d9')
    fig.patch.set_facecolor('#0f1117')

    steps = [
        {'name':'A→B','type':'Isotherme T₁','W_J':round(W_AB,2),'Q_J':round(Q_AB,2),'dU_J':round(dU_AB,2)},
        {'name':'B→C','type':'Adiabatique','W_J':round(W_BC,2),'Q_J':round(Q_BC,2),'dU_J':round(dU_BC,2)},
        {'name':'C→D','type':'Isotherme T₂','W_J':round(W_CD,2),'Q_J':round(Q_CD,2),'dU_J':round(dU_CD,2)},
        {'name':'D→A','type':'Adiabatique','W_J':round(W_DA,2),'Q_J':round(Q_DA,2),'dU_J':round(dU_DA,2)},
    ]

    return jsonify({
        'eta_pct': round(eta*100, 2),
        'eta_verif_pct': round(eta_verif*100, 2),
        'VA_L': round(VA*1e3,3), 'VB_L': round(VB*1e3,3),
        'VC_L': round(VC*1e3,3), 'VD_L': round(VD*1e3,3),
        'W_net_J': round(W_net,2),
        'Q1_J': round(Q_AB,2),
        'dU_cycle': round(dU_cycle,4),
        'steps': steps,
        'plot': fig_to_b64(fig)
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
