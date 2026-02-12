import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto 20/80 v11.8", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$999$13" 

def get_ora_ro():
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%d-%m %H:%M")

@st.cache_data(ttl=2)
def incarca_tot_fast():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                if not isinstance(date, dict): return {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}
                return date
        except: return {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}
    return {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}

def salveaza_tot(date_complete):
    with open(DB_FILE, "w") as f: json.dump(date_complete, f)
    st.cache_data.clear()

date_sistem = incarca_tot_fast()

def log_generare(metoda, variante):
    timestamp = get_ora_ro()
    if "generari" not in date_sistem: date_sistem["generari"] = []
    for var in variante:
        date_sistem["generari"].insert(0, {"ora": timestamp, "metoda": metoda, "numere": sorted(var)})
    salveaza_tot(date_sistem)

# --- DESIGN ---
st.title("🍀 Loto 20/80 v11.8")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# SIDEBAR ADMIN
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 ISTORIC GENERĂRI"):
        if date_sistem.get("generari"):
            st.dataframe(pd.DataFrame(date_sistem["generari"]), use_container_width=True)
            if st.button("🗑️ Reset"): date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()

# --- TAB-URI PRINCIPALE ---
# Adăugăm tab-ul JOC 6/49 chiar înainte de Arhivă
tab1, tab_f2, tab2, tab_649, tab3 = st.tabs(["🎯 STRATEGIE", "🔥 FIERBINȚI 2", "🎲 MIXER", "🍀 JOC 6/49", "📜 ARHIVĂ"])

with tab1:
    date_loto = date_sistem.get("extrageri", [])
    if len(date_loto) >= 3:
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3))
        fierbinti_3 = [n for n, f in Counter(numere_3).items() if f >= 2]
        toate_ist = [n for sub in date_loto for n in sub]
        pool_tot = list(set(toate_ist))
        fierbinti_ist = [n for n, f in Counter(toate_ist).items() if f >= 3]
        pool_foc_ist = list(set(fierbinti_ist + [n for n, f in Counter(toate_ist).items() if f == 2]))

        if st.button("🚀 REGELE (90%)", use_container_width=True):
            vars = [random.sample(pool_3, 4) for _ in range(18)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
        
        st.write("") 
        if st.button("🔥 MIX FIERBINȚI", use_container_width=True):
            vars = [random.sample(fierbinti_3 + pool_3, 4) for _ in range(9)]
            log_generare("Fierbinți", vars)
            for v in vars: st.error(f"🔥 {sorted(v)}")

        if st.button("📊 CALD/RECE ISTORIC", use_container_width=True):
            vars = [random.sample(pool_foc_ist, 4) for _ in range(9)]
            log_generare("Cald/Rece Istoric", vars)
            for v in vars: st.warning(f"📊 {sorted(v)}")

        if st.button("🎰 RANDOM 3", use_container_width=True):
            vars = [random.sample(pool_3, 4) for _ in range(9)]
            log_generare("Random 3", vars)
            for v in vars: st.info(f"🎲 {sorted(v)}")

        if st.button("🌎 RANDOM TOTAL", use_container_width=True):
            vars = [random.sample(pool_tot, 4) for _ in range(9)]
            log_generare("Random Total", vars)
            for v in vars: st.info(f"🌎 {sorted(v)}")
    else: st.warning("Minim 3 extrageri!")

with tab_f2:
    # ... [Păstrăm codul Fierbinți 2 neschimbat] ...
    st.subheader("🛠️ Strategii Avansate (2+2)")
    # (Aici codul tau pentru Fierbinti 2 ramane intact)

with tab2:
    # ... [Păstrăm Mixerul neschimbat] ...
    st.subheader("🎲 Mixer Manual")

with tab_649:
    st.subheader("🍀 Generator 6/49 (Random Amestecat)")
    st.write("Generează 6 numere unice dintr-un total de 49.")
    
    # Stil pentru butonul VERDE
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #28a745;
            color: white;
            border-radius: 10px;
        }
        </style>""", unsafe_allow_html=True)
    
    if st.button("🟢 GENEREAZĂ BILET 6/49", use_container_width=True):
        urna_649 = list(range(1, 50))
        random.shuffle(urna_649) # Amestecăm bine "marfa"
        varianta_649 = random.sample(urna_649, 6)
        
        # Logăm generarea (metoda 6/49)
        log_generare("6/49 Random", [varianta_649])
        
        st.success(f"🍀 Numerele tale 6/49: **{sorted(varianta_649)}**")
        st.snow()

with tab3:
    st.dataframe(pd.DataFrame(date_sistem.get("extrageri", [])), use_container_width=True)























