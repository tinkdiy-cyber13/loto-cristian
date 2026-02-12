import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto Pro v11.7", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$777$13" 

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
st.title("🍀 Loto Pro v11.7")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# SIDEBAR ADMIN
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 ISTORIC GENERĂRI"):
        if date_sistem.get("generari"):
            st.dataframe(pd.DataFrame(date_sistem["generari"]), use_container_width=True)
            if st.button("🗑️ Șterge Istoric"):
                date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()

    with st.expander("⚙️ GESTIONARE DATE", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă:")
        if st.button("💾 Salvează"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare!")

# --- LOGICA DATE ---
date_loto = date_sistem.get("extrageri", [])
if len(date_loto) >= 10:
    # Pregatire Pool-uri
    u3 = [n for sub in date_loto[:3] for n in sub]
    u10 = [n for sub in date_loto[:10] for n in sub]
    toate = [n for sub in date_loto for n in sub]
    
    # Fierbinti (apar de cel putin 2 ori in ultimele 3)
    fierbinti = [n for n, f in Counter(u3).items() if f >= 2]
    # Reci (numere din 1-80 care NU au iesit in ultimele 10)
    reci = [n for n in range(1, 81) if n not in u10]
    # Calde (cele mai frecvente din ultimele 10, dar nu neaparat fierbinti)
    calde = [n for n, f in Counter(u10).items() if f >= 4]
    # Vecini ultima extragere
    ultima = date_loto[0]
    vecini = []
    for n in ultima:
        if n > 1: vecini.append(n-1)
        if n < 80: vecini.append(n+1)
    vecini = list(set(vecini))

# --- TAB-URI ---
tab1, tab_f2, tab2, tab3 = st.tabs(["🎯 STRATEGIE", "🔥 FIERBINȚI 2", "🎲 MIXER", "📜 ARHIVĂ"])

with tab1:
    if len(date_loto) >= 3:
        pool_3 = list(set(u3))
        if st.button("🚀 REGELE (90%)"):
            vars = [random.sample(pool_3, 4) for _ in range(5)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
    else: st.warning("Minim 3 extrageri!")

with tab_f2:
    st.subheader("🛠️ Strategii Avansate (2+2)")
    if len(date_loto) >= 10:
        colA, colB = st.columns(2)
        with colA:
            if st.button("1️⃣ 2F + 2 U10"):
                vars = [random.sample(fierbinti, 2) + random.sample(u10, 2) for _ in range(5)]
                log_generare("2F + 2U10", vars)
                for v in vars: st.error(f"1: {sorted(v)}")

            if st.button("2️⃣ 2F + 2 RECI"):
                vars = [random.sample(fierbinti, 2) + random.sample(reci, 2) for _ in range(5)]
                log_generare("2F + 2Reci", vars)
                for v in vars: st.error(f"2: {sorted(v)}")

        with colB:
            if st.button("3️⃣ 2F + 2 VECINI"):
                vars = [random.sample(fierbinti, 2) + random.sample(vecini, 2) for _ in range(5)]
                log_generare("2F + 2Vecini", vars)
                for v in vars: st.error(f"3: {sorted(v)}")

            if st.button("4️⃣ 2F + 2 CALDE"):
                vars = [random.sample(fierbinti, 2) + random.sample(calde, 2) for _ in range(5)]
                log_generare("2F + 2Calde", vars)
                for v in vars: st.error(f"4: {sorted(v)}")
        
        st.divider()
        if st.button("5️⃣ 3 FIERBINȚI (Special)"):
            vars = [random.sample(fierbinti, 3) for _ in range(3)]
            log_generare("3 Fierbinti", vars)
            for v in vars: st.warning(f"5: {sorted(v)}")
    else:
        st.warning("Ai nevoie de minim 10 extrageri pentru FIERBINȚI 2!")

with tab2:
    input_m = st.text_input("Numerele tale:")
    if st.button("🎰 Mix Manual"):
        try:
            mele = [int(n) for n in input_m.split()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

with tab3:
    st.dataframe(pd.DataFrame(date_loto), use_container_width=True)


















