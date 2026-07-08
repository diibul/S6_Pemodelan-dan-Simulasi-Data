import streamlit as st
import random
import numpy as np
import pandas as pd

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

PRODUCT_PRICE = 100

# --------------------------------------------------
# KONSTANTA SEED GLOBAL
# Ubah nilai ini untuk mengubah seed di seluruh app.
# --------------------------------------------------
AGENT_SEED = 42   # seed untuk inisialisasi populasi agen
LOOP_SEED  = 99   # seed untuk urutan keputusan acak dalam loop Monte Carlo

st.set_page_config(
    page_title="Simulasi Perilaku Pembelian Pelanggan",
    layout="wide"
)

def create_agents(num_agents, shopping_mood):

    agents = []

    for i in range(num_agents):

        agent = {

            "purchase_probability": random.uniform(0.1, 0.5),

            "interest_level": random.uniform(0.0, 1.0),

            "budget": random.uniform(50, 500),

            "shopping_mood": shopping_mood,

            "self_control": random.uniform(0.0, 1.0)
        }

        agents.append(agent)

    return agents

def simulate_purchase_mood(agent, discount):

    P = agent["purchase_probability"]

    I = agent["interest_level"]

    B = agent["budget"]

    M = agent["shopping_mood"]

    P_final = P + (I * discount) + (M * 0.2)

    P_final = min(P_final, 1)

    final_price = PRODUCT_PRICE * (1 - discount)

    if B < final_price:
        return 0

    r = random.random()

    if r < P_final:
        return 1

    return 0


def apply_intervention(
    agent,
    intervention_type=None,
    iteration=0,
    threshold=0.7,
    strength=0.5,
    interval=10
):
    """
    Menerapkan mekanisme intervensi pada probabilitas pembelian agen
    untuk satu iterasi, tanpa mengubah atribut asli agen secara permanen.

    Jenis intervensi:
    - 'cooling_off'     : Reaktif — aktif jika interest_level > threshold.
    - 'budget_reminder' : Preventif — aktif setiap 'interval' iterasi.
    - None              : Tidak ada intervensi (skenario baseline).

    Formula: P_intervened = P - (strength x self_control), min 0.0
    """

    modified_prob = agent["purchase_probability"]

    if intervention_type == "cooling_off":
        if agent["interest_level"] > threshold:
            reduction = strength * agent["self_control"]
            modified_prob = max(0.0, modified_prob - reduction)

    elif intervention_type == "budget_reminder":
        if interval > 0 and (iteration % interval == 0):
            reduction = strength * agent["self_control"]
            modified_prob = max(0.0, modified_prob - reduction)

    return modified_prob


def run_simulation(
    discount_rate,
    shopping_mood,
    num_agents,
    num_iterations,
    intervention_type=None,
    intervention_strength=0.5,
    intervention_threshold=0.7,
    intervention_interval=10,
    use_seed=True
):

    discount = discount_rate / 100

    if use_seed:
        random.seed(AGENT_SEED)
        np.random.seed(AGENT_SEED)

    agents = create_agents(
        num_agents,
        shopping_mood
    )

    if use_seed:
        random.seed(LOOP_SEED)
        np.random.seed(LOOP_SEED)

    transactions_list = []

    for iteration in range(num_iterations):

        transactions = 0

        for agent in agents:

            modified_prob = apply_intervention(
                agent,
                intervention_type=intervention_type,
                iteration=iteration,
                threshold=intervention_threshold,
                strength=intervention_strength,
                interval=intervention_interval
            )

            agent_modified = {**agent, "purchase_probability": modified_prob}

            buy = simulate_purchase_mood(
                agent_modified,
                discount
            )

            transactions += buy

        transactions_list.append(transactions)

    return transactions_list


def create_agents_scenario(
    num_agents,
    mood_min=0.0,
    mood_max=1.0,
    self_control_min=0.0,
    self_control_max=1.0,
    seed=AGENT_SEED
):
    """
    Membuat populasi agen dengan rentang shopping_mood dan self_control
    yang dapat dikonfigurasi untuk tiap skenario.
    Seed menggunakan konstanta global AGENT_SEED (default) untuk reproducibility.
    """
    random.seed(seed)
    np.random.seed(seed)

    agents = []
    for _ in range(num_agents):
        agent = {
            "purchase_probability": random.uniform(0.1, 0.5),
            "interest_level":       random.uniform(0.0, 1.0),
            "budget":               random.uniform(50, 500),
            "shopping_mood":        random.uniform(mood_min, mood_max),
            "self_control":         random.uniform(self_control_min, self_control_max)
        }
        agents.append(agent)
    return agents


def _run_loop(agents, discount, num_iterations,
             intervention_type=None, strength=0.5,
             threshold=0.7, interval=10, seed=LOOP_SEED):
    """Loop simulasi internal — digunakan oleh run_all_scenarios."""
    random.seed(seed)
    np.random.seed(seed)
    transactions_list = []
    for iteration in range(num_iterations):
        transactions = 0
        for agent in agents:
            modified_prob = apply_intervention(
                agent,
                intervention_type=intervention_type,
                iteration=iteration,
                threshold=threshold,
                strength=strength,
                interval=interval
            )
            agent_mod = {**agent, "purchase_probability": modified_prob}
            transactions += simulate_purchase_mood(agent_mod, discount)
        transactions_list.append(transactions)
    return transactions_list


def run_all_scenarios(
    discount_rate,
    num_agents,
    num_iterations,
    intervention_strength=0.5,
    intervention_threshold=0.7,
    intervention_interval=10
):
    """
    Menjalankan 5 skenario what-if secara berurutan dengan seed yang sama
    agar perbandingan antar skenario fair (bukan noise acak berbeda).

    Skenario:
    1. Baseline            — populasi normal, tanpa intervensi
    2. Reaktif             — populasi normal, cooling_off
    3. Preventif           — populasi normal, budget_reminder
    4a. Distorsi Tinggi    — populasi sensitif, tanpa intervensi
    4b. Distorsi Tinggi+   — populasi sensitif, dengan intervensi reaktif
    """
    discount = discount_rate / 100
    # Menggunakan konstanta global AGENT_SEED dan LOOP_SEED

    # Populasi normal (mood & self_control seragam)
    pop_normal = create_agents_scenario(
        num_agents,
        mood_min=0.0, mood_max=1.0,
        self_control_min=0.0, self_control_max=1.0,
        seed=AGENT_SEED
    )
    # Populasi distorsi tinggi: mood tinggi (0.7-1.0) + self_control rendah (0.0-0.3)
    pop_distorsi = create_agents_scenario(
        num_agents,
        mood_min=0.7, mood_max=1.0,
        self_control_min=0.0, self_control_max=0.3,
        seed=AGENT_SEED
    )

    scenarios = {
        "Baseline (Tanpa Intervensi)": _run_loop(
            pop_normal, discount, num_iterations,
            intervention_type=None, seed=LOOP_SEED
        ),
        "Reaktif (Cooling-Off)": _run_loop(
            pop_normal, discount, num_iterations,
            intervention_type="cooling_off",
            strength=intervention_strength,
            threshold=intervention_threshold,
            seed=LOOP_SEED
        ),
        "Preventif (Budget Reminder)": _run_loop(
            pop_normal, discount, num_iterations,
            intervention_type="budget_reminder",
            strength=intervention_strength,
            interval=intervention_interval,
            seed=LOOP_SEED
        ),
        "Distorsi Tinggi (Tanpa Intervensi)": _run_loop(
            pop_distorsi, discount, num_iterations,
            intervention_type=None, seed=LOOP_SEED
        ),
        "Distorsi Tinggi (Dengan Intervensi)": _run_loop(
            pop_distorsi, discount, num_iterations,
            intervention_type="cooling_off",
            strength=intervention_strength,
            threshold=intervention_threshold,
            seed=LOOP_SEED
        ),
    }

    return scenarios


# ==================================================
# HEADER
# ==================================================

st.title("Dashboard Simulasi Perilaku Pembelian Pelanggan")

st.caption(
    "Pemodelan dan Simulasi Data | Agent-Based Modeling pada E-Commerce"
)

st.subheader("Agent-Based Modeling pada E-Commerce")

st.markdown("""
Dashboard ini digunakan untuk mensimulasikan perilaku pembelian pelanggan
berdasarkan beberapa faktor utama yang memengaruhi keputusan pembelian.

Faktor yang digunakan dalam simulasi:

- Discount Rate
- Shopping Mood
- Jumlah Agent
- Jumlah Iterasi Monte Carlo
""")

st.divider()

tab_simulasi, tab_skenario = st.tabs(
    ["📊 Simulasi Individual", "🔬 Perbandingan 4 Skenario What-If"]
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Parameter Simulasi")

discount_rate = st.sidebar.slider(
    "Discount Rate (%)",
    min_value=0,
    max_value=50,
    value=30
)

shopping_mood = st.sidebar.slider(
    "Shopping Mood",
    min_value=0.0,
    max_value=1.0,
    value=0.5
)

num_agents = st.sidebar.number_input(
    "Jumlah Agent",
    min_value=10,
    max_value=500,
    value=100
)

num_iterations = st.sidebar.number_input(
    "Jumlah Iterasi",
    min_value=100,
    max_value=5000,
    value=1000
)

st.sidebar.markdown("---")
st.sidebar.subheader("Mekanisme Intervensi")

intervention_options = {
    "Tanpa Intervensi (Baseline)": None,
    "Reaktif (Cooling-Off)": "cooling_off",
    "Preventif (Budget Reminder)": "budget_reminder"
}

intervention_label = st.sidebar.selectbox(
    "Jenis Intervensi",
    options=list(intervention_options.keys()),
    index=0
)
intervention_type_code = intervention_options[intervention_label]

intervention_strength = st.sidebar.slider(
    "Kekuatan Intervensi",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

if intervention_type_code == "cooling_off":
    intervention_threshold = st.sidebar.slider(
        "Ambang Interest Level (Reaktif)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05
    )
    intervention_interval = 10
elif intervention_type_code == "budget_reminder":
    intervention_interval = int(st.sidebar.number_input(
        "Interval Intervensi (Iterasi)",
        min_value=1,
        max_value=100,
        value=10
    ))
    intervention_threshold = 0.7
else:
    intervention_threshold = 0.7
    intervention_interval = 10

use_fixed_seed = st.sidebar.checkbox(
    "Gunakan Seed Tetap (Reproducible)",
    value=True,
    help=f"Aktif: hasil identik setiap run (AGENT_SEED={AGENT_SEED}, LOOP_SEED={LOOP_SEED}). "
         "Nonaktif: hasil bervariasi setiap run untuk eksplorasi."
)

run_button = st.sidebar.button(
    "Jalankan Simulasi"
)

st.sidebar.markdown("---")

st.sidebar.subheader("Informasi Model")

st.sidebar.write(f"Jumlah Agent : {num_agents}")
st.sidebar.write(f"Jumlah Iterasi : {num_iterations}")
st.sidebar.write(f"Seed Aktif    : {'Ya' if use_fixed_seed else 'Tidak'} "
                 f"(A={AGENT_SEED}, L={LOOP_SEED})")

if run_button:

    results = run_simulation(
        discount_rate,
        shopping_mood,
        num_agents,
        num_iterations,
        intervention_type=intervention_type_code,
        intervention_strength=intervention_strength,
        intervention_threshold=intervention_threshold,
        intervention_interval=intervention_interval,
        use_seed=use_fixed_seed
    )

    mean_value = round(np.mean(results), 2)

    max_value = int(np.max(results))

    min_value = int(np.min(results))

    std_value = round(np.std(results), 2)

else:

    mean_value = "-"

    max_value = "-"

    min_value = "-"

    std_value = "-"

# ==================================================
# TAB 1 — SIMULASI INDIVIDUAL
# ==================================================

with tab_simulasi:

    st.header("Hasil Simulasi")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rata-rata Transaksi", mean_value)

    with col2:
        st.metric("Maksimum", max_value)

    with col3:
        st.metric("Minimum", min_value)

    with col4:
        st.metric("Standar Deviasi", std_value)

    st.divider()
    st.subheader("Grafik Monte Carlo")

    if run_button:

        chart_data = pd.DataFrame({
            "Iterasi": range(1, len(results) + 1),
            "Jumlah Transaksi": results
        })
        st.line_chart(chart_data.set_index("Iterasi"))

    else:
        st.info(
            "Grafik hasil simulasi akan ditampilkan setelah simulasi dijalankan."
        )

    st.subheader("Ringkasan Hasil")

    if run_button:

        summary_df = pd.DataFrame({
            "Statistik": [
                "Rata-rata Transaksi", "Maksimum",
                "Minimum", "Standar Deviasi"
            ],
            "Nilai": [mean_value, max_value, min_value, std_value]
        })
        st.dataframe(summary_df, use_container_width=True)

    else:
        st.info(
            "Ringkasan statistik simulasi akan ditampilkan pada bagian ini."
        )

    if run_button:
        st.subheader("Kesimpulan Simulasi")
        st.write(
            f"""
            Berdasarkan hasil simulasi Monte Carlo sebanyak
            {num_iterations} iterasi dengan jumlah agent
            {num_agents}, discount rate sebesar
            {discount_rate}% dan shopping mood
            {shopping_mood:.2f},

            diperoleh rata-rata transaksi sebesar
            {mean_value} transaksi.

            Nilai maksimum yang tercapai adalah
            {max_value} transaksi dan minimum
            {min_value} transaksi dengan standar
            deviasi sebesar {std_value}.

            Mekanisme intervensi yang digunakan: **{intervention_label}**.
            Hasil ini menunjukkan bahwa model mampu
            mensimulasikan pengaruh intervensi terhadap perilaku
            pembelian pelanggan secara konsisten berdasarkan
            parameter yang diberikan.
            """
        )
        st.divider()

# ==================================================
# TAB 2 — PERBANDINGAN 4 SKENARIO WHAT-IF
# ==================================================

with tab_skenario:

    st.header("Perbandingan 4 Skenario What-If")
    st.markdown("""
    Panel ini menjalankan **5 sub-skenario** secara otomatis menggunakan parameter
    Discount Rate, Jumlah Agent, dan Jumlah Iterasi dari sidebar, dengan seed tetap
    agar perbandingan antar skenario adil (bukan perbedaan noise acak).

    | Skenario | Populasi | Intervensi |
    |----------|----------|------------|
    | 1. Baseline | Normal | Tanpa intervensi |
    | 2. Reaktif | Normal | Cooling-Off |
    | 3. Preventif | Normal | Budget Reminder |
    | 4a. Distorsi Tinggi | Mood tinggi + Self-Control rendah | Tanpa intervensi |
    | 4b. Distorsi Tinggi + Intervensi | Mood tinggi + Self-Control rendah | Cooling-Off |
    """)

    run_all_button = st.button(
        "Jalankan Perbandingan Semua Skenario",
        type="primary"
    )

    if run_all_button:

        with st.spinner("Menjalankan 5 skenario... harap tunggu."):
            all_results = run_all_scenarios(
                discount_rate=discount_rate,
                num_agents=int(num_agents),
                num_iterations=int(num_iterations),
                intervention_strength=intervention_strength,
                intervention_threshold=intervention_threshold,
                intervention_interval=intervention_interval
            )

        # --- Bangun tabel perbandingan ---
        baseline_mean = np.mean(all_results["Baseline (Tanpa Intervensi)"])
        rows = []
        for scenario_name, txn_list in all_results.items():
            mean_txn = round(np.mean(txn_list), 2)
            delta_pct = round((mean_txn / baseline_mean - 1) * 100, 1) \
                        if scenario_name != "Baseline (Tanpa Intervensi)" else "—"
            rows.append({
                "Skenario": scenario_name,
                "Rata-rata Transaksi": mean_txn,
                "Std Dev": round(np.std(txn_list), 2),
                "Maks": int(np.max(txn_list)),
                "Min": int(np.min(txn_list)),
                "Δ vs Baseline (%)": delta_pct
            })

        comparison_df = pd.DataFrame(rows)

        st.subheader("Tabel Perbandingan Kuantitatif")
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        # --- Bar chart berdampingan ---
        st.subheader("Grafik Perbandingan Rata-rata Transaksi")
        bar_df = pd.DataFrame({
            "Skenario": list(all_results.keys()),
            "Rata-rata Transaksi": [
                round(np.mean(v), 2) for v in all_results.values()
            ]
        }).set_index("Skenario")
        st.bar_chart(bar_df)

        # --- Insight otomatis ---
        st.subheader("Insight Analisis")

        mean_reaktif   = np.mean(all_results["Reaktif (Cooling-Off)"])
        mean_preventif = np.mean(all_results["Preventif (Budget Reminder)"])
        mean_dist_no   = np.mean(all_results["Distorsi Tinggi (Tanpa Intervensi)"])
        mean_dist_int  = np.mean(all_results["Distorsi Tinggi (Dengan Intervensi)"])

        best_intervention = "Reaktif" if mean_reaktif < mean_preventif else "Preventif"
        dist_reduction_pct = round((mean_dist_int / mean_dist_no - 1) * 100, 1)
        std_effectiveness  = "masih efektif" \
            if dist_reduction_pct < -5 else "kurang efektif (perlu strength lebih besar)"

        st.info(
            f"""**Skenario paling efektif menekan transaksi:** {best_intervention} """
            f"""(rata-rata {min(mean_reaktif, mean_preventif):.2f} transaksi, """
            f"""vs baseline {baseline_mean:.2f}).\n\n"""
            f"""**Efektivitas terhadap Distorsi Tinggi:** Intervensi standar """
            f"""(strength={intervention_strength}) """
            f"""{std_effectiveness} untuk populasi distorsi tinggi — """
            f"""mampu menekan transaksi sebesar {abs(dist_reduction_pct)}% """
            f"""(dari {mean_dist_no:.2f} → {mean_dist_int:.2f} transaksi)."""
        )

    else:
        st.info(
            "Klik tombol di atas untuk menjalankan dan membandingkan "
            "kelima skenario secara bersamaan."
        )

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "Muhammad Iqbal Fadel | 202310370311268 | Pemodelan dan Simulasi Data"
)