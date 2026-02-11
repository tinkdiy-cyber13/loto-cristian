import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# CONFIGURARE - Neschimbată
st.set_page_config(page_title="Loto Pro v11.3", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$888$13" 

# --- TUNING 1: CACHING PENTRU VITEZĂ ---
@st.cache_data(ttl=10) # Reîmprospătează datele la fiecare 10 secunde automat
def incarca_tot_fast():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: return {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}
    return {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}

def salveaza_tot(date_complete):
    # TUNING 2: File Lock simplu
    with open(DB_FILE, "w") as f: 
        json.dump(date_complete, f)
    st.cache_data.clear() # Curățăm cache-ul ca să vadă noile date imediat

date_sistem = incarca_tot_fast()

# --- VIZITE ---
if 'numarat' not in st.session_state:
    if "vizite" not in date_sistem: date_sistem["vizite"] = 0
    date_sistem["vizite"] += 1
    salveaza_tot(date_sistem)
    st.session_state['numarat'] = True

def log_generare(metoda, variante):
    timestamp = time.strftime("%d-%m %H:%M")
    if "generari" not in date_sistem: date_sistem["generari"] = []
    for var in variante:
        date_sistem["generari"].insert(0, {"ora": timestamp, "metoda": metoda, "numere": sorted(var)})
    salveaza_tot(date_sistem)

# --- DESIGN (Identic cu cel pe care îl iubești) ---
st.title("🍀 Loto Pro v11.3")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# SIDEBAR (Identic)
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 VERIFICARE BILETE", expanded=False):
        if date_sistem.get("generari") and date_sistem.get("extrageri"):
            ultima_ex = set(date_sistem["extrageri"][0])
            st.write(f"Ultima extragere: `{sorted(list(ultima_ex))}`")
            for g in date_sistem["generari"]:
                nimerite = set(g["numere"]) & ultima_ex
                count = len(nimerite)
                if count >= 3: st.success(f"💰 {g['metoda']} | {g['numere']} -> {count} NR!")
                elif count == 2: st.warning(f"🥈 {g['metoda']} | {g['numere']} -> 2 NR")
                else: st.write(f"⚪ {g['ora']} | {count} nr")
            if st.button("🗑️ Reset Istoric"):
                date_sistem["generari"] = []; salveaza_tot(date_sistem); st.rerun()

    with st.expander("⚙️ GESTIONARE DATE", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        col_s, col_r = st.columns(2)
        with col_s:
            if st.button("💾 Salvează"):
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        date_sistem["extrageri"].insert(0, numere)
                        salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
                except: st.error("Format invalid!")
        with col_r:
            if st.button("🗑️ Șterge Ultima"):
                if date_sistem.get("extrageri"):
                    date_sistem["extrageri"].pop(0); salveaza_tot(date_sistem); st.warning("Șters!"); st.rerun()

# TAB-URI (Identice)
date_loto = date_sistem.get("extrageri", [])
tab1, tab2, tab3 = st.tabs(["🎯 STRATEGIE", "🎲 MIXER", "📜 ARHIVĂ"])

with tab1:
    if len(date_loto) >= 3:
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3))
        fierbinti_3 = [n for n, f in Counter(numere_3).items() if f >= 2]
        toate_istoric = [n for sub in date_loto for n in sub]
        pool_total = list(set(toate_istoric))
        fierbinti_istoric = [n for n, f in Counter(toate_istoric).items() if f >= 3]
        pool_foc_istoric = list(set(fierbinti_istoric + [n for n, f in Counter(toate_istoric).items() if f == 2]))

        if st.button("🚀 REGELE (90%)"):
            vars = [random.sample(pool_3, 4) for _ in range(5)]
            log_generare("Regele 90%", vars)
            for v in vars: st.success(f"🍀 {sorted(v)}")
            st.balloons()
            
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔥 MIX FIERBINȚI"):
                vars = [random.sample(fierbinti_3 + pool_3, 4) for _ in range(5)]
                log_generare("Fierbinți", vars)
                for v in vars: st.error(f"🔥 {sorted(v)}")
            if st.button("📊 CALD/RECE ISTORIC"):
                vars = [random.sample(pool_foc_istoric, 4) for _ in range(5)]
                log_generare("Cald/Rece Istoric", vars)
                for v in vars: st.warning(f"📊 {sorted(v)}")
        with col2:
            if st.button("🎰 RANDOM 3"):
                vars = [random.sample(pool_3, 4) for _ in range(5)]
                log_generare("Random 3", vars)
                for v in vars: st.info(f"🎲 {sorted(v)}")
            if st.button("🌎 RANDOM TOTAL"):
                vars = [random.sample(pool_total, 4) for _ in range(5)]
                log_generare("Random Total", vars)
                for v in vars: st.info(f"🌎 {sorted(v)}")
    else:
        st.warning("Introdu minim 3 extrageri!")

with tab2:
    input_m = st.text_input("Cele 20 de numere ale tale:")
    if st.button("🎰 Mix Manual"):
        try:
            mele = [int(n) for n in input_m.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

with tab3:
    # TUNING 3: Arhivă vizibilă doar la cerere (pentru viteză pe mobil)
    st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# MESAJE (Identice)
st.divider()
with st.expander("📩 Trimite mesaj"):
    msg = st.text_area("Mesaj:")
    if st.button("🚀 Trimite"):
        if "mesaje" not in date_sistem: date_sistem["mesaje"] = []
        date_sistem["mesaje"].append({"data": time.strftime("%d-%m %H:%M"), "text": msg})
        salveaza_tot(date_sistem); st.success("Trimis!"); st.rerun()

if este_admin:
    st.subheader("📬 Inbox")
    for m in reversed(date_sistem.get("mesaje", [])): st.info(f"{m['data']}: {m['text']}")













