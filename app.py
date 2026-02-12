import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto 20/80 v11.8.2", page_icon="🎰", layout="centered")

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

# --- CSS PENTRU BUTOANE RESTRÂNSE (Mici și compacte) ---
st.markdown("""
    <style>
    div.stButton > button {
        height: 2.2em !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }
    #btn_649_verde {
        color: #28a745 !important;
        border: 2px solid #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLU ȘI OO ---
st.title("🍀 Loto 20/80 v11.8.2")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 ISTORIC"):
        if date_sistem.get("generari"):
            st.dataframe(pd.DataFrame(date_sistem["generari"]), use_container_width=True)
            if st.button("🗑️ Reset"): date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()

# --- LOGICA DATE ---
date_loto = date_sistem.get("extrageri", [])
if len(date_loto) >= 10:
    u3 = [n for sub in date_loto[:3] for n in sub]
    u10 = [n for sub in date_loto[:10] for n in sub]
    fierbinti_u3 = [n for n, f in Counter(u3).items() if f >= 2]
    reci = [n for n in range(1, 81) if n not in u10]
    calde = [n for n, f in Counter(u10).items() if f >= 4]
    vecini = []
    for n in date_loto[0]: # Doar ultima extragere
        if n > 1: vecini.append(n-1)
        if n < 80: vecini.append(n+1)
    vecini = list(set(vecini))

# --- TAB-URI ---
tab1, tab_f2, tab2, tab_649, tab3 = st.tabs(["🎯 STRATEGIE", "🔥 FIERBINȚI 2", "🎲 MIXER", "🍀 JOC 6/49", "📜 ARHIVĂ"])

with tab1:
    if len(date_loto) >= 3:
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3))
        
        # Buton mare de start
        if st.button("🚀 REGELE (90%)", use_container_width=True):
            vars = [random.sample(pool_3, 4) for _ in range(18)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
        
        # Butoane restrânse în coloane
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 FIERBINȚI", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 4) if len(fierbinti_u3)>=4 else random.sample(pool_3,4) for _ in range(9)]
                log_generare("Fierbinti", vars)
                for v in vars: st.error(f"🔥 {sorted(v)}")
            if st.button("📊 CALD/RECE", use_container_width=True):
                vars = [random.sample(pool_3, 4) for _ in range(9)]
                log_generare("Cald/Rece", vars)
                for v in vars: st.warning(f"📊 {sorted(v)}")
        with c2:
            if st.button("🎲 RANDOM 3", use_container_width=True):
                vars = [random.sample(pool_3, 4) for _ in range(9)]
                log_generare("Random 3", vars)
                for v in vars: st.info(f"🎲 {sorted(v)}")
            if st.button("🌎 4/80", use_container_width=True):
                vars = [random.sample(range(1,81), 4) for _ in range(9)]
                log_generare("4/80", vars)
                for v in vars: st.info(f"🌎 {sorted(v)}")
    else: st.warning("Minim 3 extrageri!")

with tab_f2:
    if len(date_loto) >= 10:
        colA, colB = st.columns(2)
        with colA:
            if st.button("1️⃣ 2F+2U10", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 2) + random.sample(u10, 2) for _ in range(5)]
                log_generare("2F+2U10", vars)
                for v in vars: st.error(f"1: {sorted(v)}")
            if st.button("2️⃣ 2F+2RECI", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 2) + random.sample(reci, 2) for _ in range(5)]
                log_generare("2F+2Reci", vars)
                for v in vars: st.error(f"2: {sorted(v)}")
        with colB:
            if st.button("3️⃣ 2F+2VECI", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 2) + random.sample(vecini, 2) for _ in range(5)]
                log_generare("2F+2Vecini", vars)
                for v in vars: st.error(f"3: {sorted(v)}")
            if st.button("4️⃣ 2F+2CALD", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 2) + random.sample(calde, 2) for _ in range(5)]
                log_generare("2F+2Calde", vars)
                for v in vars: st.error(f"4: {sorted(v)}")
        if st.button("5️⃣ 3 FIERBINȚI", use_container_width=True):
            vars = [random.sample(fierbinti_u3, 3) for _ in range(9)]
            log_generare("3Fierbinti", vars)
            for v in vars: st.warning(f"5: {sorted(v)}")

with tab_649:
    st.subheader("🍀 JOC 6/49")
    c649_1, c649_2 = st.columns(2)
    with c649_1:
        if st.button("🟢 GENEREAZĂ 6/49", use_container_width=True, key="btn_649"):
            v = sorted(random.sample(range(1, 50), 6)) for _ in range(5))
            log_generare("6/49", [v])
            st.success(f"Bilet: {v}")
            st.snow()

with tab2:
    input_m = st.text_input("Numerele tale:", key="m_in")
    if st.button("🎰 Amestecă", use_container_width=True):
        try:
            mele = [int(n) for n in input_m.split()]
            for i in range(10): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

with tab3:
    st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

if este_admin:
    with st.expander("⚙️ GESTIUNE DATE"):
        raw = st.text_input("Extragere nouă:")
        if st.button("💾 Salvează"):
            numere = [int(n) for n in raw.replace(",", " ").split() if n.strip().isdigit()]
            if len(numere) == 20:
                date_sistem["extrageri"].insert(0, numere)
                salveaza_tot(date_sistem); st.rerun()




















