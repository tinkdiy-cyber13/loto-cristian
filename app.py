import streamlit as st
import pandas as pd
from collections import Counter
import random
import json
import os

# Configurare Mobil
st.set_page_config(page_title="Loto Pro v9.1", page_icon="🔐", layout="centered")

DB_FILE = "baza_date_cristian.json"
PAROLA_ADMIN = "admin123" # <--- SCHIMBĂ PAROLA AICI!

def incarca_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def salveaza_date(date):
    with open(DB_FILE, "w") as f:
        json.dump(date, f)

st.title("🚀 Loto Cristian v9.1")

# --- SISTEM DE AUTENTIFICARE ---
st.sidebar.subheader("🔐 Acces Admin")
parola_introdusa = st.sidebar.text_input("Introdu Parola:", type="password")
este_admin = (parola_introdusa == PAROLA_ADMIN)

if este_admin:
    st.sidebar.success("Ești conectat ca Admin!")
else:
    st.sidebar.warning("Introdu parola pentru a gestiona datele.")

# --- 1. GESTIONARE DATE (Protejat) ---
if este_admin:
    with st.expander("➕ Adaugă / Șterge Extrageri (PROTEJAT)", expanded=True):
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

# --- 2. MIXER MANUAL (La vedere) ---
st.divider()
with st.expander("🎲 Mixerul Meu Manual (20 nr -> 5 var)"):
    input_manual = st.text_input("Pune aici cele 20 de numere ale TALE:")
    if st.button("🎰 Amestecă Numerele Mele"):
        try:
            mele = [int(n) for n in input_manual.replace(",", " ").split() if n.strip().isdigit()]
            if len(mele) >= 4:
                for i in range(5):
                    st.success(f"V{i+1}: {sorted(random.sample(mele, 4))}")
            else: st.error("Pune măcar 4 numere!")
        except: st.error("Eroare!")

# --- 3. ANALIZA SI GENERARE ---
date_loto = incarca_date()
if date_loto:
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎰 MIX AUTO", "📊 STRATEGIE", "📜 ARHIVĂ"])
    
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

    with tab3:
        if este_admin:
            st.subheader("📜 Istoric Extrageri")
            for idx, ex in enumerate(date_loto):
                st.text(f"{idx+1}. {ex}")
        else:
            st.error("⚠️ Arhiva este protejată. Introdu parola în meniul din stânga.")
else:
    st.info("Baza de date e goală.")


