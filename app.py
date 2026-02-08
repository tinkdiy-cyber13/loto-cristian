import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v9.3", page_icon="🎁", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin123" 

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v9.3")

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Panou Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.expander("⚙️ GESTIONARE DATE (ACTIV)", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă:")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Salvează"):
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_curente = incarca_date()
                    date_curente.insert(0, numere); salveaza_date(date_curente[:20])
                    st.success("✅ Salvat!"); st.rerun()
        with col_b:
            if st.button("🗑️ Șterge Ultima"):
                date_curente = incarca_date()
                if date_curente:
                    date_curente.pop(0); salveaza_date(date_curente)
                    st.warning("Șters!"); st.rerun()

# --- MIXER MANUAL ---
st.divider()
with st.expander("🎲 Mixer Manual"):
    input_manual = st.text_input("Pune cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

# --- ANALIZA ȘI ARHIVA ---
date_loto = incarca_date()
if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STRATEGIE", "📜 REZULTATE"])
    
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
        st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# --- 🎁 BUTONUL SURPRIZĂ (NOU!) ---
st.divider()
st.write("### ✨ Ceva special?")
if st.button("🎁 APASĂ PENTRU SURPRIZĂ"):
    with st.spinner("Se încarcă norocul..."):
        time.sleep(1.5)
    st.balloons() # Efect de animație pe ecran
    
    mesaje = [
        "Cristian, cu i5-ul ăsta și mintea ta, ești de neoprit! 🚀",
        "Norocul și-l face omul cu mâna lui (și cu Python)! 🐍",
        "Ești oficial cel mai tehnologizat jucător de loto! 🎰",
        "Berea aia de care ziceai? Să fie una câștigătoare! 🍻",
        "11 este pe drum, simt eu! 🎯"
    ]
    st.info(random.choice(mesaje))
    st.snow() # Efect de zăpadă/particule



