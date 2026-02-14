import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time
from datetime import datetime, timedelta

# CONFIGURARE
st.set_page_config(page_title="Loto Pro v11.9.6", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$111$13"

def get_ora_ro():
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%d-%m %H:%M")

@st.cache_data(ttl=2)
def incarca_tot_fast():
    default = {"extrageri": [], "vizite": 0, "mesaje": [], "generari": []}
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                if not isinstance(date, dict): return default
                # Asigurăm prezența cheilor
                for k in default:
                    if k not in date: date[k] = default[k]
                return date
        except: return default
    return default

def salveaza_tot(date_complete):
    with open(DB_FILE, "w") as f: json.dump(date_complete, f)
    st.cache_data.clear()

date_sistem = incarca_tot_fast()

# --- VIZITE ---
if 'numarat' not in st.session_state:
    date_sistem["vizite"] = date_sistem.get("vizite", 0) + 1
    salveaza_tot(date_sistem)
    st.session_state['numarat'] = True

def log_generare(metoda, variante):
    timestamp = get_ora_ro()
    if "generari" not in date_sistem: date_sistem["generari"] = []
    for var in variante:
        date_sistem["generari"].insert(0, {"ora": timestamp, "metoda": metoda, "numere": sorted(var)})
    salveaza_tot(date_sistem)

# --- CSS STYLING ---
st.markdown("""
    <style>
    div.stButton > button { height: 2.2em !important; font-size: 14px !important; font-weight: bold !important; }
    div.stButton > button[key="btn_gold"] {
        background-color: #FFD700 !important; color: #000000 !important;
        border: 2px solid #FFA500 !important; box-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5) !important;
    }
    #btn_649_v { color: #28a745 !important; border: 2px solid #28a745 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & OO ---
st.title("🍀 Loto Pro v11.9.5")
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.sidebar.expander("📋 VERIFICARE AUTO"):
        if date_sistem["generari"] and date_sistem["extrageri"]:
            ultima = set(date_sistem["extrageri"][0])
            for g in date_sistem["generari"]:
                n = set(g["numere"]) & ultima
                if len(n) >= 3: st.success(f"💰 {len(n)} NR! {g['numere']}")
                elif len(n) == 2: st.warning(f"🥈 2 NR {g['numere']}")
    
    with st.expander("⚙️ GESTIONARE DATE"):
        raw = st.text_input("Introdu 20 nr (spațiu între):")
        if st.button("💾 Salvează"):
            numere = [int(n) for n in raw.replace(",", " ").split() if n.strip().isdigit()]
            if len(numere) == 20:
                date_sistem["extrageri"].insert(0, numere); salveaza_tot(date_sistem); st.rerun()
        st.divider()
        if st.button("🧹 Curăță (Păstrează 13)"):
            date_sistem["extrageri"] = date_sistem["extrageri"][:13]; salveaza_tot(date_sistem); st.rerun()

# --- LOGICA DATE ---
date_loto = date_sistem["extrageri"]
u3 = [n for sub in date_loto[:3] for n in sub] if len(date_loto) >= 3 else []
u10 = [n for sub in date_loto[:10] for n in sub] if len(date_loto) >= 10 else []

# --- TAB-URI ---
tab1, tab_f2, tab2, tab_649, tab3 = st.tabs(["🎯 STRATEGIE", "🔥 FIERBINȚI 2", "🎲 MIXER", "🍀 JOC 6/49", "📜 ARHIVĂ"])

with tab1:
    if len(date_loto) >= 3:
        pool3 = list(set(u3))
        if st.button("👑 REGELE (90%)", use_container_width=True):
            v = [random.sample(pool3, 4) for _ in range(5)]; log_generare("Rege", v); st.balloons()
            for i in v: st.success(sorted(i))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 FIERBINȚI", use_container_width=True):
                v = [random.sample(u3, 4) for _ in range(5)]; log_generare("Fierb", v)
                for i in v: st.error(sorted(i))
        with c2:
            if st.button("🎲 RANDOM 3", use_container_width=True):
                v = [random.sample(pool3, 4) for _ in range(5)]; log_generare("R3", v)
                for i in v: st.info(sorted(i))
    else: st.warning("Ai nevoie de minim 3 extrageri în Arhivă!")

with tab_f2:
    if len(date_loto) >= 10:
        fierb_u3 = [n for n, f in Counter(u3).items() if f >= 2]
        cA, cB = st.columns(2)
        with cA:
            if st.button("1️⃣ 2F+2U10", use_container_width=True):
                v = [random.sample(fierb_u3, 2) + random.sample(u10, 2) for _ in range(5)]
                log_generare("2F+2U10", v); [st.error(sorted(i)) for i in v]
        with cB:
            if st.button("🥇 3 FIERBINȚI GOLD", use_container_width=True, key="btn_gold"):
                v = [random.sample(fierb_u3, 3) for _ in range(5)]
                log_generare("3GOLD", v); st.balloons()
                for i in v: st.info(f"💎 {sorted(i)}")
    else: st.warning("Ai nevoie de minim 10 extrageri pentru acest tab!")

with tab2:
    input_mixer = st.text_input("Cele 20 de numere ale tale:")
    if st.button("🎰 Mixer Manual", use_container_width=True):
        mele = [int(n) for n in input_mixer.split() if n.strip().isdigit()]
        if len(mele) >= 4:
            for i in range(5): st.success(sorted(random.sample(mele, 4)))

with tab_649:
    if st.button("🟢 GENEREAZĂ 6/49", use_container_width=True, key="btn_649_v"):
        v = [sorted(random.sample(range(1, 50), 6)) for _ in range(5)]
        log_generare("6/49", v); [st.success(i) for i in v]; st.snow()

with tab3:
    if date_loto:
        df = pd.DataFrame(date_loto)
        df.columns = [f"Nr.{i+1}" for i in range(20)]
        zile = ["L", "Ma", "Mi", "J", "V", "S", "D"]
        ieri = datetime.utcnow() + timedelta(hours=2) - timedelta(days=1)
        df.index = [f"{zile[(ieri - timedelta(days=(i//2))).weekday()]}{i+1}" for i in range(len(df))]
        st.dataframe(df, use_container_width=True)
    else: st.info("Arhiva e goală. Mergi la Admin și adaugă extrageri!")

# --- MESAJE ---
st.divider()
with st.expander("📩 Trimite mesaj"):
    msg = st.text_area("Mesaj:")
    if st.button("🚀 Trimite"):
        date_sistem["mesaje"].append({"data": time.strftime("%d-%m %H:%M"), "text": msg})
        salveaza_tot(date_sistem); st.success("Trimis!"); st.rerun()

if este_admin:
    st.subheader("📬 Inbox")
    for m in reversed(date_sistem["mesaje"]): st.info(f"{m['data']}: {m['text']}")



































