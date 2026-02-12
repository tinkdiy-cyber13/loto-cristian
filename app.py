import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto Pro v11.8.1", page_icon="🎰", layout="centered")

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
st.title("🍀 Loto Pro v11.8.1")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# SIDEBAR ADMIN (Tabel Istoric & Verificare)
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 ISTORIC GENERĂRI"):
        if date_sistem.get("generari"):
            st.dataframe(pd.DataFrame(date_sistem["generari"]), use_container_width=True)
            if st.button("🗑️ Reset Istoric"): date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()
    with st.sidebar.expander("📋 VERIFICARE BILETE"):
        if date_sistem.get("generari") and date_sistem.get("extrageri"):
            ultima_ex = set(date_sistem["extrageri"][0]) if date_sistem["extrageri"] else set()
            for g in date_sistem["generari"]:
                nimerite = set(g["numere"]) & ultima_ex
                count = len(nimerite)
                if count >= 3: st.success(f"💰 {g['metoda']} | {count} NR!")
                elif count == 2: st.warning(f"🥈 {g['metoda']} | 2 NR")
                else: st.write(f"⚪ {g['ora']} | {count} nr")

# --- TAB-URI PRINCIPALE ---
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

        if st.button("🚀 REGELE (90%)", use_container_width=True, key="btn_rege"):
            vars = [random.sample(pool_3, 4) for _ in range(18)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
        
        st.write("") 
        if st.button("🔥 MIX FIERBINȚI", use_container_width=True, key="btn_fierb"):
            vars = [random.sample(fierbinti_3 + pool_3, 4) for _ in range(9)]
            log_generare("Fierbinți", vars)
            for v in vars: st.error(f"🔥 {sorted(v)}")
        if st.button("📊 CALD/RECE ISTORIC", use_container_width=True, key="btn_ist"):
            vars = [random.sample(pool_foc_ist, 4) for _ in range(9)]
            log_generare("Cald/Rece Istoric", vars)
            for v in vars: st.warning(f"📊 {sorted(v)}")
        if st.button("🎰 RANDOM 3", use_container_width=True, key="btn_r3"):
            vars = [random.sample(pool_3, 4) for _ in range(9)]
            log_generare("Random 3", vars)
            for v in vars: st.info(f"🎲 {sorted(v)}")
        if st.button("🌎 RANDOM TOTAL", use_container_width=True, key="btn_rt"):
            vars = [random.sample(pool_tot, 4) for _ in range(9)]
            log_generare("Random Total", vars)
            for v in vars: st.info(f"🌎 {sorted(v)}")
    else: st.warning("Minim 3 extrageri!")

with tab_f2:
    st.subheader("🛠️ Strategii Avansate (2+2)")
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

        if len(fierbinti_u3) >= 2:
            colA, colB = st.columns(2)
            with colA:
                if st.button("1️⃣ 2F + 2 U10"):
                    vars = [random.sample(fierbinti_u3, 2) + random.sample(u10, 2) for _ in range(5)]
                    log_generare("2F+2U10", vars)
                    for v in vars: st.error(f"1: {sorted(v)}")
                if st.button("2️⃣ 2F + 2 RECI"):
                    vars = [random.sample(fierbinti_u3, 2) + random.sample(reci, 2) for _ in range(5)]
                    log_generare("2F+2Reci", vars)
                    for v in vars: st.error(f"2: {sorted(v)}")
            with colB:
                if st.button("3️⃣ 2F + 2 VECINI"):
                    vars = [random.sample(fierbinti_u3, 2) + random.sample(vecini, 2) for _ in range(5)]
                    log_generare("2F+2Vecini", vars)
                    for v in vars: st.error(f"3: {sorted(v)}")
                if st.button("4️⃣ 2F + 2 CALDE"):
                    vars = [random.sample(fierbinti_u3, 2) + random.sample(calde, 2) for _ in range(5)]
                    log_generare("2F+2Calde", vars)
                    for v in vars: st.error(f"4: {sorted(v)}")
            st.divider()
            if st.button("5️⃣ 3 FIERBINȚI (3 VAR)"):
                vars = [random.sample(fierbinti_u3, 3) for _ in range(3)]
                log_generare("3Fierbinti", vars)
                for v in vars: st.warning(f"5: {sorted(v)}")
    else: st.warning("Introdu minim 10 extrageri!")

with tab2:
    st.subheader("🎲 Mixer Manual")
    input_m = st.text_input("Cele 50 de numere ale tale:", key="mixer_input")
    if st.button("🎰 Amestecă", key="btn_mixer"):
        try:
            mele = [int(n) for n in input_m.split()]
            if len(mele) >= 4:
                for i in range(10): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

with tab_649:
    st.subheader("🍀 Generator 6/49 (Verde)")
    # Butonul Verde doar pentru acest tab
    st.markdown("""<style>div.stButton > button#btn_649_verde {
        color: #28a745 !important; border: 2px solid #28a745 !important; font-weight: bold !important;
    }</style>""", unsafe_allow_html=True)
    
    if st.button("🟢 GENEREAZĂ 6/49", use_container_width=True, key="btn_649_verde"):
        urna = list(range(1, 50))
        random.shuffle(urna)
        var = random.sample(urna, 6)
        log_generare("6/49 Random", [var])
        st.success(f"🍀 Bilet 6/49: **{sorted(var)}**")
        st.snow()

with tab3:
    st.dataframe(pd.DataFrame(date_sistem.get("extrageri", [])), use_container_width=True)

# GESTIONARE DATE (ADMIN)
if este_admin:
    with st.expander("⚙️ GESTIONARE DATE", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă:")
        if st.button("💾 Salvează"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare!")

















