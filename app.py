import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v10.2", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$clover$13" 

def incarca_tot():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                if isinstance(date, list): return {"extrageri": date, "vizite": 0, "mesaje": []}
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

st.title("🚀 Loto Pro v10.2")

# --- AFISARE SIMBOL "OO" ---
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Panou Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.expander("⚙️ GESTIONARE DATE", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        if st.button("💾 Salvează"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    if "extrageri" not in date_sistem: date_sistem["extrageri"] = []
                    date_sistem["extrageri"].insert(0, numere)
                    salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
            except: st.error("Eroare format!")
        if st.button("🗑️ Șterge Ultima"):
            if date_sistem.get("extrageri"):
                date_sistem["extrageri"].pop(0); salveaza_tot(date_sistem); st.warning("Șters!"); st.rerun()

# --- TAB-URI PRINCIPALE ---
date_loto = date_sistem.get("extrageri", [])
tab1, tab2, tab3 = st.tabs(["🎯 STRATEGIE", "🎲 MIXERE", "📜 ARHIVĂ"])

with tab1:
    st.header("🎯 Strategia Cristian")
    if len(date_loto) >= 3:
        # Extragem numerele din ultimele 3 trageri
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3)) # Numere unice din ultimele 3
        
        st.write(f"🔎 Bazat pe ultimele 3 extrageri (Pool: {len(pool_3)} numere)")
        
        if st.button("🚀 GENEREAZĂ VARIANTE (Regula 90%)"):
            st.subheader("🍀 Variante propuse:")
            for i in range(5):
                # Generăm variante de 4 numere STRICT din cele apărute în ultimele 3 trageri
                varianta = sorted(random.sample(pool_3, 4))
                st.success(f"Bilet {i+1}: {varianta}")
            st.snow()
    else:
        st.warning("Ai nevoie de minim 3 extrageri în arhivă pentru această strategie!")

with tab2:
    st.subheader("Alte Mixere")
    if date_loto:
        toate_istoric = [n for sub in date_loto for n in sub]
        pool_total = list(set(toate_istoric))
        
        if st.button("🎰 Mix Random Total (Toată Arhiva)"):
            for i in range(5): st.info(f"R-{i+1}: {sorted(random.sample(pool_total, 4))}")
            
        if st.button("📊 Strategie Cald/Rece (Istoric)"):
            numaratoare = Counter(toate_istoric)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            pool_foc = list(set(fierbinti + [n for n, f in numaratoare.items() if f == 2]))
            for i in range(5): st.warning(f"S-{i+1}: {sorted(random.sample(pool_foc, 4))}")

with tab3:
    st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# --- 📩 MESAJE ---
with st.expander("📩 Trimite mesaj"):
    msg = st.text_area("Mesaj anonim:")
    if st.button("🚀 Trimite"):
        nou_msg = {"data": time.strftime("%d-%m %H:%M"), "text": msg}
        if "mesaje" not in date_sistem: date_sistem["mesaje"] = []
        date_sistem["mesaje"].append(nou_msg); salveaza_tot(date_sistem)
        st.success("Trimis!"); st.rerun()

if este_admin:
    st.divider()
    st.subheader("📬 Inbox")
    for m in reversed(date_sistem.get("mesaje", [])):
        st.info(f"{m['data']}: {m['text']}")












