import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto 20/80 v11.8.5", page_icon="🎰", layout="centered")

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

# --- REPARARE CONTOR OO (Aici era lipsa) ---
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
    div.stButton > button {
        height: 2.2em !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLU ȘI OO ---
st.title("🍀 Loto 20/80 v11.8.5")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    # --- 1. VERIFICATORUL AUTOMAT (Sub Parolă) ---
    with st.sidebar.expander("📋 VERIFICARE BILETE (AUTO)", expanded=True):
        if date_sistem.get("generari") and date_sistem.get("extrageri"):
            u_ex = date_sistem["extrageri"][0] if isinstance(date_sistem["extrageri"][0], list) else date_sistem["extrageri"]
            ultima_ex = set(u_ex)
            st.write(f"Verificăm cu: `{sorted(list(ultima_ex))}`")
            for g in date_sistem["generari"]:
                nimerite = set(g["numere"]) & ultima_ex
                count = len(nimerite)
                if count >= 3:
                    st.success(f"💰 {g['metoda']} | {g['numere']} -> {count} NR!")
                elif count == 2:
                    st.warning(f"🥈 {g['metoda']} | {g['numere']} -> 2 NR")
                else:
                    st.write(f"⚪ {g['ora']} | {count} nr")
        else:
            st.info("Nicio generare sau extragere nouă.")

    # --- 2. ISTORICUL TABELAR ---
    with st.sidebar.expander("📋 ISTORIC TABEL"):
        if date_sistem.get("generari"):
            df_istoric = pd.DataFrame(date_sistem["generari"])
            df_istoric['numere'] = df_istoric['numere'].astype(str)
            st.dataframe(df_istoric, use_container_width=True)
            if st.button("🗑️ Reset Complet Istoric", key="reset_final_v101"): 
                date_sistem["generari"] = []
                salveaza_tot(date_sistem)
                st.rerun()

    # --- 3. GESTIONARE DATE (REPARAT ALINIEREA AICI) ---
    with st.expander("⚙️ GESTIONARE DATE", expanded=False):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):", key="input_extragere_v101")
        if st.button("💾 Salvează Extragerea", key="save_extragere_v101"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem)
                    st.success("✅ Salvat!"); st.rerun()
                else:
                    st.error("Pune fix 20 de numere!")
            except:
                st.error("Eroare format!")
                
    # --- 3. GESTIONARE DATE (Unde bagi extragerea nouă) ---
    with st.expander("⚙️ GESTIONARE DATE", expanded=False):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        # ALTĂ CHEIE UNICĂ PENTRU BUTONUL DE SALVARE
        if st.button("💾 Salvează Extragerea", key="salveaza_extragere_unique"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem)
                    st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare format!")


    # --- 3. GESTIONARE DATE (Unde bagi extragerea nouă) ---
    with st.expander("⚙️ GESTIONARE DATE (BAGĂ EXTRAGEREA)"):
       raw_input = st.text_input("Introdu extragerea nouă (20 nr):", key="input_admin_unic")
        if st.button("💾 Salvează Extragerea"):
            try:numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem)
                    st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare format!")

    # --- 2. ISTORICUL TABELAR (Sub Verificator) ---
    with st.sidebar.expander("📋 ISTORIC TABEL"):
        if date_sistem.get("generari"):
            df_istoric = pd.DataFrame(date_sistem["generari"])
            df_istoric['numere'] = df_istoric['numere'].astype(str)
            st.dataframe(df_istoric, use_container_width=True)
            if st.button("🗑️ Reset Complet"): 
                date_sistem["generari"] = []
                salveaza_tot(date_sistem)
                st.rerun()

    # --- 3. GESTIONARE DATE (Unde bagi extragerea nouă) ---
    with st.expander("⚙️ GESTIONARE DATE (BAGĂ EXTRAGEREA)"):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        if st.button("💾 Salvează Extragerea"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem)
                    st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare format!")

# --- LOGICA DATE ---
date_loto = date_sistem.get("extrageri", [])
if len(date_loto) >= 10:
    u3 = [n for sub in date_loto[:3] for n in sub]
    u10 = [n for sub in date_loto[:10] for n in sub]
    fierbinti_u3 = [n for n, f in Counter(u3).items() if f >= 2]
    reci = [n for n in range(1, 81) if n not in u10]
    calde = [n for n, f in Counter(u10).items() if f >= 4]
    vecini = []
    # FIX: Verificăm dacă există extrageri înainte de a accesa indexul 0
    if date_loto:
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
            vars = [random.sample(pool_3, 4) for _ in range(18)]
            log_generare("Regele 90%", vars); st.balloons()
            for v in vars: st.success(f"🍀 {sorted(v)}")
        
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
       # --- TUNING SPECIAL BUTONUL 5 GOLD ---
        st.divider()
        st.markdown("""<style> div.stButton > button[key="btn_3_fierbinti_gold"] {
            background-color: #FFD700 !important; 
            color: #000000 !important; 
            border: 2px solid #FFA500 !important; 
            box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.6) !important;
            font-size: 16px !important;
        }</style>""", unsafe_allow_html=True)

        if st.button("🥇 3 FIERBINȚI (Sistem Gold)", use_container_width=True, key="btn_3_fierbinti_gold"):
            if len(fierbinti_u3) >= 3:
                vars = [random.sample(fierbinti_u3, 3) for _ in range(5)]
                log_generare("3 FIERBINTI GOLD", vars)
                st.balloons()
                for v in vars:
                    st.info(f"💎 **{sorted(v)}**")
            else:
                st.warning("Așteptăm să se 'încingă' numerele (minim 3 necesare)!")

with tab_649:
    st.subheader("🍀 JOC 6/49 - 5 Variante")
    st.markdown("""<style> div.stButton > button[key="btn_649_verde"] {
        color: #28a745 !important; border: 2px solid #28a745 !important; font-weight: bold !important;
    }</style>""", unsafe_allow_html=True)

    if st.button("🟢 GENEREAZĂ 5 VAR. 6/49", use_container_width=True, key="btn_649_verde"):
        variante_649 = []
        for _ in range(5):
            urna = list(range(1, 50))
            random.shuffle(urna)
            v = sorted(random.sample(urna, 6))
            variante_649.append(v)
        log_generare("6/49 Random", variante_649)
        for i, var in enumerate(variante_649):
            st.success(f"Bilet {i+1}: {var}")
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
            try:
                numere = [int(n) for n in raw.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem); st.rerun()
            except: st.error("Format invalid!")





































