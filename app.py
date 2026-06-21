import streamlit as st
import random
import numpy as np
import pandas as pd

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

PRODUCT_PRICE = 100

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

            "shopping_mood": shopping_mood
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

def run_simulation(
    discount_rate,
    shopping_mood,
    num_agents,
    num_iterations
):

    discount = discount_rate / 100

    agents = create_agents(
        num_agents,
        shopping_mood
    )

    transactions_list = []

    for iteration in range(num_iterations):

        transactions = 0

        for agent in agents:

            buy = simulate_purchase_mood(
                agent,
                discount
            )

            transactions += buy

        transactions_list.append(transactions)

    return transactions_list

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

run_button = st.sidebar.button(
    "Jalankan Simulasi"
)

st.sidebar.markdown("---")

st.sidebar.subheader("Informasi Model")

st.sidebar.write(f"Jumlah Agent : {num_agents}")
st.sidebar.write(f"Jumlah Iterasi : {num_iterations}")

if run_button:

    results = run_simulation(
        discount_rate,
        shopping_mood,
        num_agents,
        num_iterations
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
# HASIL SIMULASI
# ==================================================


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

# ==================================================
# GRAFIK
# ==================================================

st.subheader("Grafik Monte Carlo")

if run_button:

    chart_data = pd.DataFrame({
        "Iterasi": range(1, len(results) + 1),
        "Jumlah Transaksi": results
    })

    st.line_chart(
        chart_data.set_index("Iterasi")
    )

else:

    st.info(
        "Grafik hasil simulasi akan ditampilkan setelah simulasi dijalankan."
    )

# ==================================================
# TABEL HASIL
# ==================================================

st.subheader("Ringkasan Hasil")

if run_button:

    summary_df = pd.DataFrame({

        "Statistik": [
            "Rata-rata Transaksi",
            "Maksimum",
            "Minimum",
            "Standar Deviasi"
        ],

        "Nilai": [
            mean_value,
            max_value,
            min_value,
            std_value
        ]
    })

    st.dataframe(
        summary_df,
        use_container_width=True
    )

else:

    st.info(
        "Ringkasan statistik simulasi akan ditampilkan pada bagian ini."
    )

# ==================================================
# KESIMPULAN
# ==================================================

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

        Hasil ini menunjukkan bahwa model mampu
        mensimulasikan perilaku pembelian pelanggan
        secara konsisten berdasarkan parameter yang diberikan.
        """
    )

    st.divider()

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "Muhammad Iqbal Fadel | 202310370311268 | Pemodelan dan Simulasi Data"
)