import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto 20/80 v10.3", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$888$13" 

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

st.title("🍀 Loto 20/80 v10.3")

# --- AFISARE SIMBOL "OO" ---
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL ---
st.sidebar.subheader("🔐 Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.expander("⚙️ GESTIONARE DATE", expanded=True):
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        col_s, col_r = st.columns(2)
        with col_s:
            if st.button("💾 Salvează"):
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        if "extrageri" not in date_sistem: date_sistem["extrageri"] = []
                        date_sistem["extrageri"].insert(0, numere)
                        salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
                except: st.error("Eroare format!")
        with col_r:
            if st.button("🗑️ Șterge Ultima"):
                if date_sistem.get("extrageri"):
                    date_sistem["extrageri"].pop(0); salveaza_tot(date_sistem); st.warning("Șters!"); st.rerun()

# --- TAB-URI ---
date_loto = date_sistem.get("extrageri", [])
tab1, tab2, tab3 = st.tabs(["🎯 STRATEGIA TA", "🎲 MIXER MANUAL", "📜 ARHIVĂ"])

with tab1:
    st.subheader("🔥 Butoane Generare")
    if len(date_loto) >= 3:
        # Pregătire date pentru Strategia Cristian (ultimele 3)
        numere_3 = [n for sub in date_loto[:3] for n in sub]
        pool_3 = list(set(numere_3))
        numaratoare_3 = Counter(numere_3)
        fierbinti_3 = [n for n, f in numaratoare_3.items() if f >= 2]
        
        # Pregătire date pentru Strategie Istoric (toate)
        toate_istoric = [n for sub in date_loto for n in sub]
        pool_total = list(set(toate_istoric))
        numaratoare_istoric = Counter(toate_istoric)
        fierbinti_istoric = [n for n, f in numaratoare_istoric.items() if f >= 3]
        pool_foc_istoric = list(set(fierbinti_istoric + [n for n, f in numaratoare_istoric.items() if f == 2]))

        # --- BUTONUL REGE (CRISTIAN 90%) ---
        if st.button("🚀 GENEREAZĂ DIN ULTIMELE 3 (Regula 90%)"):
            st.write("✨ Variante din Pool-ul de moment:")
            for i in range(5):
                st.success(f"Bilet {i+1}: {sorted(random.sample(pool_3, 4))}")
            st.balloons()

        st.divider()

        # --- RESTUL DE BUTOANE ---
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔥 MIX 3 FIERBINȚI"):
                for i in range(5): st.error(f"F3-{i+1}: {sorted(random.sample(fierbinti_3 + pool_3, 4))}")
            
            if st.button("📊 CALD/RECE ISTORIC"):
                for i in range(5): st.warning(f"S-{i+1}: {sorted(random.sample(pool_foc_istoric, 4))}")

        with col2:
            if st.button("🎰 MIX RANDOM 3"):
                for i in range(5): st.info(f"L3-{i+1}: {sorted(random.sample(pool_3, 4))}")

            if st.button("🌎 RANDOM TOTAL"):
                for i in range(5): st.info(f"R-{i+1}: {sorted(random.sample(pool_total, 4))}")
    else:
        st.warning("Ai nevoie de minim 3 extrageri salvate!")

with tab2:
    st.subheader("🎲 Mixer Manual (20 nr ale tale)")
    input_manual = st.text_input("Pune cele 20 de numere:")
    if st.button("🎰 Amestecă"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
        except: st.error("Eroare!")

with tab3:
    st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# --- MESAJE SI SURPRIZA ---
st.divider()
col_m1, col_m2 = st.columns(2)
with col_m1:
    with st.expander("📩 Trimite mesaj"):
        msg = st.text_area("Mesaj anonim:")
        if st.button("🚀 Trimite"):
            nou_msg = {"data": time.strftime("%d-%m %H:%M"), "text": msg}
            if "mesaje" not in date_sistem: date_sistem["mesaje"] = []
            date_sistem["mesaje"].append(nou_msg); salveaza_tot(date_sistem)
            st.success("Trimis!"); st.rerun()
with col_m2:
    if st.button("🎁 SURPRIZĂ"):
        st.snow()
        st.balloons()
        mesaje_funny = [
            "Sistemul zice că ești la un bilet distanță de căstig ! 💻",
            "Dacă iese 11 diseară, dăm liber la bere! 🍻",
            "Algoritmul a calculat: Norocul tău e mai mare decât baza de date! 📈",
            "Atenție! Excesul de numere norocoase poate provoca zâmbete! 😁",
            "Nu eu aleg numerele, ele te aleg pe tine! ✨",
            "Baza de date e plină, dar portofelul mai are loc! 💰",
            "Folosește-l cu cap! 🎩",
            "În caz de câștig,joaca incontinuare 🤖",
            "Statistica zice că cine nu joacă, nu câștigă.🐍",
            "Berea e rece, norocul e pe drum! 🚀"
        ]
        st.info(random.choice(mesaje_funny))

if este_admin:
    st.subheader("📬 Inbox")
    for m in reversed(date_sistem.get("mesaje", [])):
        st.info(f"{m['data']}: {m['text']}")



















