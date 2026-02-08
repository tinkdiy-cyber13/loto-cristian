import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v8.0", page_icon="🎰", layout="centered")

DB_FILE = "baza_date_cristian.json"

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v8.0")

# --- 1. INTRODUCERE DATE ---
with st.expander("➕ Adaugă / Gestionază Date", expanded=True):
    raw_input = st.text_input("Introdu cele 20 de numere (cu spațiu):")
    
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
                else:
                    st.error("Pune fix 20 de numere!")
            except:
                st.error("Format greșit!")
    
    with col_b:
        if st.button("🗑️ Șterge Ultima"):
            date_curente = incarca_date()
            if date_curente:
                date_curente.pop(0)
                salveaza_date(date_curente)
                st.warning("Ultima a fost ștearsă!")
                st.rerun()

# --- 2. ANALIZA SI GENERARE ---
date_loto = incarca_date()

if date_loto:
    st.divider()
    st.write(f"📊 Baza de date: **{len(date_loto)}** extrageri.")
    
    tab1, tab2, tab3 = st.tabs(["🎰 MIX RANDOM", "📊 STRATEGIE", "📜 ARHIVĂ"])
    
    with tab1:
        if st.button("GENEREAZĂ RANDOM"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            for i in range(5):
                st.subheader(f"Varianta {i+1}")
                st.success(sorted(random.sample(toate_aparute, 4)))

    with tab2:
        if st.button("CALCULEAZĂ FIERBINȚI/RECI"):
            toate = [n for sub in date_loto for n in sub]
            numaratoare = Counter(toate)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            echilibrate = [n for n, f in numaratoare.items() if f == 2]
            reci = list(set(range(1, 81)) - set(toate))
            g_a = list(set(reci + echilibrate))
            g_b = list(set(fierbinti + echilibrate))
            
            st.write("🔥 **TOP FIERBINȚI:**", sorted(fierbinti[:5]))
            st.subheader("🚀 Sugestii Foc + Echilibru")
            for _ in range(3): st.code(sorted(random.sample(g_b, 4)))
            st.subheader("❄️ Sugestii Gheață + Echilibru")
            for _ in range(3): st.code(sorted(random.sample(g_a, 4)))

    with tab3:
        st.write("Ultimele numere salvate (de la cea mai nouă):")
        for idx, ex in enumerate(date_loto):
            st.text(f"{idx+1}. {ex}")

else:
    st.info("Baza de date e goală. Adaugă primele numere de pe Lotostats!")
