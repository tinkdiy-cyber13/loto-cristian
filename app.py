import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v9.2", page_icon="📜", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin123" # <--- SCHIMBĂ PAROLA AICI!

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v9.2")

# --- SISTEM DE AUTENTIFICARE (DOAR PENTRU MODIFICĂRI) ---
st.sidebar.subheader("🔐 Panou Control Admin")
parola_introdusa = st.sidebar.text_input("Introdu Parola pentru Modificări:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

# --- 1. GESTIONARE DATE (DOAR CU PAROLĂ) ---
if este_admin:
    with st.expander("⚙️ ADMIN: Adaugă / Șterge (ACTIV)", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă (20 numere):")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Salvează"):
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        date_curente = incarca_date()
                        date_curente.insert(0, numere)
                        salveaza_date(date_curente[:20])
                        st.success("✅ Salvat!")
                        st.rerun()
                except: st.error("Eroare format!")
        with col_b:
            if st.button("🗑️ Șterge Ultima"):
                date_curente = incarca_date()
                if date_curente:
                    date_curente.pop(0)
                    salveaza_date(date_curente)
                    st.warning("Șters!")
                    st.rerun()
else:
    st.sidebar.info("Modificările sunt blocate.")

# --- 2. MIXER MANUAL ---
st.divider()
with st.expander("🎲 Mixer Manual (20 nr -> 5 var)"):
    input_manual = st.text_input("Pune aici cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5):
                    st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
            else: st.error("Minim 4 numere!")
        except: st.error("Eroare!")

# --- 3. ANALIZA ȘI ARHIVA (LA VEDERE) ---
date_loto = incarca_date()
if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STRATEGIE", "📜 REZULTATE ARHIVĂ"])
    
    with tab1:
        if st.button("GENEREAZĂ DIN ISTORIC"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            for i in range(5): st.info(sorted(random.sample(toate_aparute, 4)))

    with tab2:
        if st.button("CALCULEAZĂ"):
            toate = [n for sub in date_loto for n in sub]
            numaratoare = Counter(toate)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            g_b = list(set(fierbinti + [n for n, f in numaratoare.items() if f == 2]))
            st.write("🔥 **TOP FIERBINȚI:**", sorted(fierbinti[:5]))
            for _ in range(3): st.code(sorted(random.sample(g_b, 4)))

    with tab3:
        st.subheader("📜 Istoric Extrageri (Doar Verificare)")
        # Tabel curat pentru vizualizare
        df = pd.DataFrame(date_loto)
        df.index = [f"Extragerea {i+1}" for i in range(len(date_loto))]
        st.dataframe(df, use_container_width=True)
else:
    st.info("Baza de date e goală.")


