import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto 20/80 v11.9.4", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$333$13" 

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

# --- REPARARE CONTOR OO ---
if 'numarat' not in st.session_state:
    if "vizite" not in date_sistem: date_sistem["vizite"] = 0
    date_sistem["vizite"] += 1
    salveaza_tot(date_sistem)
    st.session_state['numarat'] = True

def log_generare(metoda, variante):
    timestamp = get_ora_ro()
    if "generari" not in date_sistem: date_sistem["generari"] = []
    for var in variante:
        date_sistem["generari"].insert(0, {"ora": timestamp, "metoda": metoda, "numere": sorted(var)})
    salveaza_tot(date_sistem)

# --- CSS BUTOANE RESTRÂNSE ---
st.markdown("""
    <style>
    div.stButton > button { height: 2.2em !important; font-size: 14px !important; font-weight: bold !important; }
    div.stButton > button[key="btn_3_fierbinti_gold"] {
        background-color: #FFD700 !important; color: #000000 !important;
        border: 2px solid #FFA500 !important; box-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLU ȘI OO ---
st.title("🍀 Loto 20/80 v11.9.4")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 VERIFICARE AUTO", expanded=True):
        if date_sistem.get("generari") and date_sistem.get("extrageri"):
            ultima_ex = set(date_sistem["extrageri"][0])
            st.write(f"Verificăm cu: `{sorted(list(ultima_ex))}`")
            for g in date_sistem["generari"]:
                nimerite = set(g["numere"]) & ultima_ex
                count = len(nimerite)
                if count >= 3: st.success(f"💰 {g['metoda']} | {count} NR!")
                elif count == 2: st.warning(f"🥈 {g['metoda']} | 2 NR")
                else: st.write(f"⚪ {count} nr")
    
    with st.sidebar.expander("📋 ISTORIC TABEL"):
        if date_sistem.get("generari"):
            df_h = pd.DataFrame(date_sistem["generari"])
            df_h['numere'] = df_h['numere'].astype(str)
            st.dataframe(df_h, use_container_width=True)
            if st.button("🗑️ Reset", key="res_i"):
                date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()

    with st.expander("⚙️ GESTIONARE DATE", expanded=False):
        raw_in = st.text_input("Introdu extragerea nouă (20 nr):", key="in_ex")
        if st.button("💾 Salvează", key="sv_ex"):
            numere = [int(n) for n in raw_in.replace(",", " ").split() if n.strip().isdigit()]
            if len(numere) == 20:
                date_sistem["extrageri"].insert(0, numere); salveaza_tot(date_sistem); st.rerun()
        st.divider()
        if st.button("🧹 Păstrează ultimele 13", key="cl_13"):
            date_sistem["extrageri"] = date_sistem["extrageri"][:13]
            salveaza_tot(date_sistem); st.rerun()

# --- LOGICA DATE ---
date_loto = date_sistem.get("extrageri", [])
if len(date_loto) >= 10:
    u3 = [n for sub in date_loto[:3] for n in sub]
    u10 = [n for sub in date_loto[:10] for n in sub]
    fierbinti_u3 = [n for n, f in Counter(u3).items() if f >= 2]
    reci = [n for n in range(1, 81) if n not in u10]
    calde = [n for n, f in Counter(u10).items() if f >= 4]
    vecini = []
    for n in date_loto[0]:
        if n > 1: vecini.append(n-1)
        if n < 80: vecini.append(n+1)
    vecini = list(set(vecini))

# --- TAB-URI ---
tab1, tab_f2, tab2, tab_649, tab3 = st.tabs(["🎯 STRATEGIE", "🔥 FIERBINȚI 2", "🎲 MIXER", "🍀 JOC 6/49", "📜 ARHIVĂ"])

with tab1:
    if len(date_loto) >= 3:
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3))
        if st.button("👑 REGELE (90%)", use_container_width=True):
            vars = [random.sample(pool_3, 4) for _ in range(5)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 FIERBINȚI", use_container_width=True):
                vars = [random.sample(fierbinti_u3, 4) if len(fierbinti_u3)>=4 else random.sample(pool_3,4) for _ in range(5)]
                log_generare("Fierbinti", vars)
                for v in vars: st.error(f"🔥 {sorted(v)}")
        with c2:
            if st.button("🎰 RANDOM 3", use_container_width=True):
                vars = [random.sample(pool_3, 4) for _ in range(5)]
                log_generare("Random 3", vars)
                for v in vars: st.info(f"🎲 {sorted(v)}")
    else: st.warning("Minim 3 extrageri!")

with tab_f2:
    if len(date_loto) >= 10:
        cA, cB = st.columns(2)
        with cA:
            if st.button("1️⃣ 2F+2U10", use_container_width=True):
                v = [random.sample(fierbinti_u3, 2) + random.sample(u10, 2) for _ in range(5)]
                log_generare("2F+2U10", v); [st.error(sorted(i)) for i in v]
        with cB:
            if st.button("3️⃣ 2F+2VECI", use_container_width=True):
                v = [random.sample(fierbinti_u3, 2) + random.sample(vecini, 2) for _ in range(5)]
                log_generare("2F+2Vecini", v); [st.error(sorted(i)) for i in v]
        if st.button("🥇 3 FIERBINȚI GOLD", use_container_width=True, key="btn_3_fierbinti_gold"):
            v = [random.sample(fierbinti_u3, 3) for _ in range(5)]
            log_generare("3Fierbinti Gold", v); st.balloons()
            for i in v: st.info(f"💎 {sorted(i)}")
    else: st.warning("Minim 10 extrageri!")

with tab_649:
    if st.button("🟢 GENEREAZĂ 5 VAR. 6/49", use_container_width=True, key="btn_649"):
        vars = [sorted(random.sample(range(1, 50), 6)) for _ in range(5)]
        log_generare("6/49", vars)
        for v in vars: st.success(f"🍀 {v}")

with tab3:
    if date_loto:
        df_a = pd.DataFrame(date_loto)
        df_a.columns = [f"Nr.{i+1}" for i in range(20)]
        zile = ["L", "Ma", "Mi", "J", "V", "S", "D"]
        ieri = datetime.utcnow() + timedelta(hours=2) - timedelta(days=1)
        idx = [f"{zile[(ieri - timedelta(days=(i//2))).weekday()]}{i+1}" for i in range(len(df_a))]
        df_a.index = idx
        st.dataframe(df_a, use_container_width=True)








































