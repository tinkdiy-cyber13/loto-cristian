import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os
import time

# Configurare Mobil
st.set_page_config(page_title="Loto 20/80 v9.9", page_icon="📩", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin13$clover$13" # Schimbă aici!

def incarca_tot():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                date = json.load(f)
                if isinstance(date, list): return {"extrageri": date, "vizite": 0, "mesaje": []}
                if "mesaje" not in date: date["mesaje"] = []
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

st.title("🚀 Loto 20/80 v9.9")

# --- AFISARE SIMBOL "OO" ---
st.markdown(f"<div style='text-align: right; margin-top: -55px;'><span style='color: #22d3ee; font-size: 16px; font-weight: bold; border: 2px solid #22d3ee; padding: 4px 12px; border-radius: 15px; background-color: rgba(34, 211, 238, 0.1);'>OO: {date_sistem.get('vizite', 0)}</span></div>", unsafe_allow_html=True)

# --- ADMIN PANEL (SIDEBAR) ---
st.sidebar.subheader("🔐 Panou Control Admin")
parola_introdusa = st.sidebar.text_input("Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    with st.expander("⚙️ GESTIONARE DATE & MESAJE", expanded=True):
        st.subheader("📬 Mesaje Primite")
        if date_sistem.get("mesaje"):
            for m in reversed(date_sistem["mesaje"]):
                st.info(f"📅 {m['data']}\n💬 {m['text']}")
            if st.button("🗑️ Șterge toate mesajele"):
                date_sistem["mesaje"] = []; salveaza_tot(date_sistem); st.rerun()
        else: st.write("Niciun mesaj nou.")
        
        st.divider()
        st.subheader("📈 Control Loto")
        raw_input = st.text_input("Introdu extragerea nouă (20 nr):")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Salvează"):
                try:
                    numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                    if len(numere) == 20:
                        if "extrageri" not in date_sistem: date_sistem["extrageri"] = []
                        date_sistem["extrageri"].insert(0, numere)
                        salveaza_tot(date_sistem); st.success("✅ Salvat!"); st.rerun()
                except: st.error("Eroare format!")
        with col_b:
            if st.button("🗑️ Șterge Ultima"):
                if date_sistem.get("extrageri"):
                    date_sistem["extrageri"].pop(0); salveaza_tot(date_sistem); st.warning("Șters!"); st.rerun()

# --- 📩 CASUTA DE MESAJE (PENTRU UTILIZATORI) ---
st.divider()
with st.expander("📩 Trimite un mesaj "):
    msg_text = st.text_area("Scrie aici mesajul tău (anonim):", height=100)
    if st.button("🚀 Trimite Mesajul"):
        if msg_text.strip():
            nou_msg = {"data": time.strftime("%d-%m %H:%M"), "text": msg_text}
            date_sistem["mesaje"].append(nou_msg)
            salveaza_tot(date_sistem)
            st.success("✅ Mesajul a fost trimis către Admin!")
            time.sleep(1); st.rerun()
        else: st.error("Scrie ceva!")

# --- MIXER MANUAL ---
st.divider()
with st.expander("🎲 Mixer Manual"):
    input_manual = st.text_input("Pune cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5): st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
            else: st.error("Minim 4 numere!")
        except: st.error("Eroare!")

# --- ANALIZA ȘI ARHIVA ---
date_loto = date_sistem.get("extrageri", [])
if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STRATEGIE", "📜 REZULTATE"])
    with tab1:
        if st.button("GENEREAZĂ DIN ISTORIC"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            for i in range(5): st.info(sorted(random.sample(toate_aparute, 4)))
    with tab2:
        if st.button("CALCULEAZĂ"):
            toate = [n for sub in date_loto for n in sub]
            numaratoare = Counter(toate)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            g_b = list(set(fierbinti + [n for n, f in numaratoare.items() if f == 2]))
            st.write("🔥 **TOP FIERBINȚI:**", sorted(fierbinti[:5]))
            for _ in range(3): st.code(sorted(random.sample(g_b, 4)))
    with tab3: st.dataframe(pd.DataFrame(date_loto), use_container_width=True)

# --- 🎁 BUTONUL SURPRIZĂ ---
st.divider()
if st.button("🎁 SURPRIZĂ"):
    st.balloons()
    st.snow()
    mesaje_funny = [
        "Sistemul zice că ești la un bilet distanță de a-ți lua un i9! 💻",
        "Dacă iese 11 diseară, dăm liber la bere! 🍻",
        "Algoritmul a calculat: Norocul tău e mai mare decât baza de date! 📈",
        "Atenție! Excesul de numere norocoase poate provoca zâmbete! 😁",
        "Nu eu aleg numerele, ele te aleg pe tine! ✨",
        "Baza de date e plină, dar portofelul mai are loc! 💰",
        "Ești oficial Admin-ul propriului noroc. Folosește-l cu cap! 🎩",
        "În caz de câștig, nu uita de procesorul i5 care a muncit aici! 🤖",
        "Statistica zice că cine nu joacă, nu câștigă. Cine joacă cu Python, sperie urna! 🐍",
        "Codul e gata, berea e rece, norocul e pe drum! 🚀"
    ]
    st.info(random.choice(mesaje_funny))

















