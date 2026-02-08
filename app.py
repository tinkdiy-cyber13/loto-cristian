import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os

# Setari pagina pentru Mobil
st.set_page_config(page_title="Loto Pro Cristian", page_icon="🎰")

DB_FILE = "baza_date_cristian.json"

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v7.0 (Web)")

# 1. INTRODUCERE DATE
with st.expander("➕ Adaugă Extragere Nouă"):
    raw_input = st.text_input("Introdu cele 20 de numere (cu spațiu):")
    if st.button("Salvează în Baza de Date"):
        try:
            numere = [int(n) for n in raw_input.replace(",", " ").split() if n.strip().isdigit()]
            if len(numere) == 20:
                date_curente = incarca_date()
                date_curente.insert(0, numere)
                salveaza_date(date_curente[:20])
                st.success("✅ Salvare reușită!")
            else:
                st.error("Trebuie să fie fix 20 de numere!")
        except:
            st.error("Format greșit!")

# 2. ANALIZA SI GENERARE
date_loto = incarca_date()

if date_loto:
    st.write(f"📊 Baza de date conține **{len(date_loto)}** extrageri.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Analiză Strategie"):
            toate = [n for sub in date_loto for n in sub]
            numaratoare = Counter(toate)
            fierbinti = [n for n, f in numaratoare.items() if f >= 3]
            echilibrate = [n for n, f in numaratoare.items() if f == 2]
            reci = list(set(range(1, 81)) - set(toate))
            
            g_a = list(set(reci + echilibrate))
            g_b = list(set(fierbinti + echilibrate))
            
            st.subheader("🔥 Mix Foc")
            for _ in range(3):
                st.code(sorted(random.sample(g_b, 4)))
            
            st.subheader("❄️ Mix Gheață")
            for _ in range(3):
                st.code(sorted(random.sample(g_a, 4)))

    with col2:
        if st.button("🎰 Mix Random"):
            toate_aparute = list(set([n for sub in date_loto for n in sub]))
            st.subheader("🎰 Rezultat Random")
            for _ in range(5):
                st.code(sorted(random.sample(toate_aparute, 4)))
else:
    st.info("Baza de date e goală. Adaugă primele numere!")