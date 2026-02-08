import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v9.5", page_icon="📈", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin123" 

# --- FUNCTII BAZA DE DATE (REPARATE) ---
def incarca_tot():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                # Daca datele sunt in format vechi (doar o lista), le convertim
                if isinstance(date, list):
                    return {"extrageri": date, "vizite": 0}
                return date
        except:
            return {"extrageri": [], "vizite": 0}
    return {"extrageri": [], "vizite": 0}

def salveaza_tot(date_complete):
    with open(DB_FILE, "w") as f:
        json.dump(date_complete, f)

# --- INITIALIZARE ---
date_sistem = incarca_tot()

# Contorizam doar la inceputul sesiunii
if 'numarat' not in st.session_state:
    vizite_actuale = date_sistem.get("vizite", 0) + 1
    date_sistem["vizite"] = vizite_actuale
    salveaza_tot(date_sistem)
    st.session_state['numarat'] = True

st.title("🚀 Loto Cristian v9.5")

# --- AFISARE CONTOR DISCRET ---
st.markdown(f"<p style='text-align: right; color: gray; font-size: 12px;'>S: {date_sistem.get('vizite', 0)}</p>", unsafe_allow_html=True)

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
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        if "extrageri" not in date_sistem: date_sistem["extrageri"] = []
                        date_sistem["extrageri"].insert(0, numere)
                        salveaza_tot(date_sistem)
                        st.success("✅ Salvat!"); st.rerun()
                except: st.error("Format numere greșit!")
        with col_b:
            if st.button("🗑️ Șterge Ultima"):
                if date_sistem.get("extrageri"):
                    date_sistem["extrageri"].pop(0)
                    salveaza_tot(date_sistem)
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
        except: st.error("Eroare la procesare!")

# --- ANALIZA ȘI ARHIVA ---
date_loto = date_sistem.get("extrageri", [])
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

# --- 🎁 BUTONUL SURPRIZĂ ---
st.divider()
if st.button("🎁 SURPRIZĂ"):
    st.balloons()
    st.info("Baftă maximă, Cristian! i5-ul tău e la butoane. 🚀")

