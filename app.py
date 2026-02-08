import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v9.0", page_icon="🔐", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ARHIVA = "admin123" # SCHIMBĂ PAROLA AICI!

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v9.0")

# --- 1. INTRODUCERE DATE ---
with st.expander("➕ Adaugă / Gestionază Date", expanded=False):
    raw_input = st.text_input("Introdu extragerea nouă (20 numere):")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Salvează"):
            try:
                numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
                if len(numere) == 20:
                    date_curente = incarca_date()
                    date_curente.insert(0, numere)
                    salveaza_date(date_curente[:20])
                    st.success("✅ Salvat!")
                    st.rerun()
            except: st.error("Eroare la numere!")
    
    with col_b:
        if st.button("🗑️ Șterge Ultima"):
            date_curente = incarca_date()
            if date_curente:
                date_curente.pop(0)
                salveaza_date(date_curente)
                st.warning("Șters!")
                st.rerun()

# --- 2. MIXERUL TĂU DE 20 NUMERE (Nou!) ---
st.divider()
with st.expander("🎲 Mixerul Meu Manual (20 nr -> 5 var)"):
    input_manual = st.text_input("Pune aici cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă Numerele Mele"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                st.subheader("🍀 Variantele Tale:")
                for i in range(5):
                    st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
            else:
                st.error("Pune măcar 4 numere!")
        except: st.error("Eroare la format!")

# --- 3. ANALIZA SI GENERARE ---
date_loto = incarca_date()

if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STRATEGIE", "📜 ARHIVĂ"])
    
    with tab1:
        if st.button("GENEREAZĂ RANDOM DIN ISTORIC"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            for i in range(5):
                st.info(sorted(random.sample(toate_aparute, 4)))

    with tab2:
        if st.button("CALCULEAZĂ FIERBINȚI/RECI"):
            toate = [n for sub in date_loto for n in sub]
            numaratoare = Counter(toate)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            reci = list(set(range(1, 81)) - set(toate))
            g_b = list(set(fierbinti + [n for n, f in numaratoare.items() if f == 2]))
            
            st.write("🔥 **TOP FIERBINȚI:**", sorted(fierbinti[:5]))
            for _ in range(3): st.code(sorted(random.sample(g_b, 4)))

    with tab3:
        st.subheader("🔐 Acces Protejat")
        parola_introdusa = st.text_input("Introdu parola pentru a vedea istoricul:", type="password")
        if parola_introdusa == PAROLA_ARHIVA:
            st.success("Acces permis!")
            for idx, ex in enumerate(date_loto):
                st.text(f"{idx+1}. {ex}")
        elif parola_introdusa != "":
            st.error("Parolă greșită!")

else:
    st.info("Baza de date e goală.")

