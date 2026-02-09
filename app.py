import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto 20/80 v10.1", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$clover$13" 

def incarca_tot():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                if isinstance(date, list): return {"extrageri": date, "vizite": 0, "mesaje": []}
                if "mesaje" not in date: date["mesaje"] = []
                return date
        except: return {"extrageri": [], "vizite": 0, "mesaje": []}
    return {"extrageri": [], "vizite": 0, "mesaje": []}

def salveaza_tot(date_complete):
    with open(DB_FILE, "w") as f: json.dump(date_complete, f)

date_sistem = incarca_tot()

if 'numarat' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_tot(date_sistem)
    st.session_state['numarat'] = True

st.title("🚀 Loto 20/80 v10.1")

# --- AFISARE SIMBOL "OO" ---
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL (SIDEBAR) ---
st.sidebar.subheader("🔐 Panou Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.expander("⚙️ GESTIONARE DATE & MESAJE", expanded=True):
        st.subheader("📬 Mesaje Primite")
        if date_sistem.get("mesaje"):
            for m in reversed(date_sistem["mesaje"]):
                st.info(f"📅 {m['data']}\n💬 {m['text']}")
            if st.button("🗑️ Șterge toate mesajele"):
                date_sistem["mesaje"] = []; salveaza_tot(date_sistem); st.rerun()
        
        st.divider()
        st.subheader("📈 Control Loto")
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Salvează"):
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        if "extrageri" not in date_sistem: date_sistem["extrageri"] = []
                        date_sistem["extrageri"].insert(0, numere)
                        salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
                except: st.error("Eroare format!")
        with col_b:
            if st.button("🗑️ Șterge Ultima"):
                if date_sistem.get("extrageri"):
                    date_sistem["extrageri"].pop(0); salveaza_tot(date_sistem); st.warning("Șters!"); st.rerun()

# --- MIXER MANUAL ---
st.divider()
with st.expander("🎲 Mixer Manual"):
    input_manual = st.text_input("Pune cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
            else: st.error("Minim 4 numere!")
        except: st.error("Eroare!")

# --- ANALIZA ȘI ARHIVA ---
date_loto = date_sistem.get("extrageri", [])
if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STATISTICI", "📜 REZULTATE"])
    
    with tab1:
        # Buton 1: Tot istoricul
        if st.button("1️⃣ GENEREAZĂ DIN TOT ISTORICUL"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            for i in range(5): st.info(sorted(random.sample(toate_aparute, 4)))
        
        st.divider()
        # Butoane 2 si 3: Ultimele 3 trageri
        if len(date_loto) >= 3:
            numere_3 = [n for sub in date_loto[:3] for n in sub]
            pool_3 = list(set(numere_3))
            numaratoare_3 = Counter(numere_3)
            fierbinti_3 = [n for n, f in numaratoare_3.items() if f >= 2]
            rest_3 = list(set(pool_3) - set(fierbinti_3))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("2️⃣ MIX ULTIMELE 3"):
                    for i in range(5): st.warning(f"L3-{i+1}: {sorted(random.sample(pool_3, 4))}")
            with col2:
                if st.button("3️⃣ 🔥 MIX 3 FIERBINȚI"):
                    pool_foc_3 = list(set(fierbinti_3 + rest_3))
                    for i in range(5): st.error(f"F3-{i+1}: {sorted(random.sample(pool_foc_3, 4))}")
        else:
            st.warning("Ai nevoie de minim 3 extrageri pentru butoanele 2 și 3!")

        st.divider()
        # Butoane 4 si 5: Strategie Cald/Rece si Random din tot
        col3, col4 = st.columns(2)
        toate_istoric = [n for sub in date_loto for n in sub]
        numaratoare_istoric = Counter(toate_istoric)
        fierbinti_istoric = [n for n, f in numaratoare_istoric.items() if f >= 3]
        g_b_istoric = list(set(fierbinti_istoric + [n for n, f in numaratoare_istoric.items() if f == 2]))
        
        with col3:
            if st.button("4️⃣ STRATEGIE CALD/RECE"):
                for i in range(5): st.success(f"S-{i+1}: {sorted(random.sample(g_b_istoric, 4))}")
        with col4:
            if st.button("5️⃣ MIX RANDOM TOTAL"):
                pool_total = list(set(toate_istoric))
                for i in range(5): st.info(f"R-{i+1}: {sorted(random.sample(pool_total, 4))}")

    with tab2:
        st.subheader("Statistici Generale")
        toate = [n for sub in date_loto for n in sub]
        numaratoare = Counter(toate)
        st.write("🔥 **TOP 5 FIERBINȚI TOTAL:**", sorted([n for n, f in numaratoare.items() if f >= 3][:5]))
        st.write("📊 Număr total extrageri procesate:", len(date_loto))
            
    with tab3: st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# --- 🎁 BUTONUL SURPRIZĂ ---
st.divider()
if st.button("🎁 SURPRIZĂ"):
    st.balloons(); st.snow()
    mesaje_funny = ["Cristian, i5-ul tău e la butoane! 💻", "11 e pe drum! 🎯", "Succes maxim! 🚀"]
    st.info(random.choice(mesaje_funny))
















