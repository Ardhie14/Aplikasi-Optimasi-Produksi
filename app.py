import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Optimasi Produksi", layout="centered")

st.title("🔧 Aplikasi Optimasi Produksi (Linear Programming)")

st.sidebar.title("📥 Input Data")

# Input jumlah produk
n = st.sidebar.number_input("Jumlah produk", min_value=2, max_value=5, step=1)

# Input nama produk
produk = [st.sidebar.text_input(f"Nama produk ke-{i+1}", value=f"P{i+1}") for i in range(n)]

# Input keuntungan
keuntungan = [st.sidebar.number_input(f"Keuntungan per unit {produk[i]}", value=10.0) for i in range(n)]

# Input batasan
m = st.sidebar.number_input("Jumlah kendala (batasan sumber daya)", min_value=1, max_value=5, step=1)

batasan = []
sumberdaya = []
for j in range(m):
    st.sidebar.markdown(f"### Kendala {j+1}")
    batasan.append([st.sidebar.number_input(f"{produk[i]} per unit untuk Kendala {j+1}", value=1.0, key=f"a{i}{j}") for i in range(n)])
    sumberdaya.append(st.sidebar.number_input(f"Total batas Kendala {j+1}", value=100.0, key=f"b{j}"))

# Hitung optimasi
if st.button("🔍 Hitung Solusi Optimal"):
    c = [-x for x in keuntungan]  # konversi ke masalah minimisasi
    A = batasan
    b = sumberdaya

    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        st.success("Solusi optimal ditemukan!")
        hasil = res.x.round(2)
        st.subheader("✅ Hasil Optimasi:")
        for i in range(n):
            st.write(f"Produksi {produk[i]} = {hasil[i]} unit")
        st.write(f"💰 Total Keuntungan Maksimum = Rp {(-res.fun):,.2f}")

        # Visualisasi area feasible jika 2 variabel
        if n == 2:
            x = np.linspace(0, max(b)*1.2, 400)
            fig, ax = plt.subplots()
            for i in range(m):
                y = (b[i] - A[i][0]*x)/A[i][1]
                ax.plot(x, y, label=f"Kendala {i+1}")
            ax.set_xlim((0, max(b)*1.2))
            ax.set_ylim((0, max(b)*1.2))
            ax.fill_between(x, 0, y, alpha=0.1)
            ax.plot(res.x[0], res.x[1], 'ro', label="Solusi Optimal")
            ax.set_xlabel(produk[0])
            ax.set_ylabel(produk[1])
            ax.legend()
            st.pyplot(fig)
    else:
        st.error("Tidak ditemukan solusi optimal. Coba cek input.")
