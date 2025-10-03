import random
import requests
import streamlit as st

API = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,languages,currencies,flags"

st.set_page_config(page_title="REST Countries — Card", page_icon="🌍", layout="centered")

@st.cache_data(show_spinner=False, ttl=3600)
def load_countries():
    resp = requests.get(API, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list) or not data:
        raise RuntimeError("No se recibieron países.")
    return data

def fmt_population(n):
    try:
        return f"{int(n):,}".replace(",", ".")
    except Exception:
        return "—"

def pick_random_country(countries):
    return random.choice(countries)

st.title("REST Countries — Card")

# Alert placeholder
alert = st.empty()

try:
    with st.spinner("Cargando países..."):
        countries = load_countries()
except Exception as e:
    alert.error(f"Error al cargar países: {e}")
    st.stop()

if "country" not in st.session_state:
    st.session_state.country = pick_random_country(countries)

def show_country(c):
    name = (c.get("name", {}).get("common") or c.get("name", {}).get("official")) or "—"
    official = c.get("name", {}).get("official", "—")
    capital = ", ".join(c.get("capital", [])) if c.get("capital") else "—"
    region = c.get("region", "—")
    subregion = c.get("subregion", "—")
    population = fmt_population(c.get("population"))
    languages = ", ".join(c.get("languages", {}).values()) if c.get("languages") else "—"
    currencies = ", ".join([v.get("name", "—") for v in c.get("currencies", {}).values()]) if c.get("currencies") else "—"
    flag = c.get("flags", {}).get("svg") or c.get("flags", {}).get("png")

    # Safe container (older Streamlit may not support border=True)
    try:
        ctx = st.container(border=True)
    except TypeError:
        ctx = st.container()

    with ctx:
        col1, col2 = st.columns([1, 2])  # bandera 1/3, datos 2/3
        with col1:
            if flag:
                try:
                    st.image(flag, width=200)
                except TypeError:
                    st.image(flag, use_column_width=True)
        with col2:
            st.subheader(name)
            st.write(f"**Nombre oficial:** {official}")
            st.write(f"**Capital:** {capital}")
            st.write(f"**Región:** {region} ({subregion})")
            st.write(f"**Población:** {population}")
            st.write(f"**Idiomas:** {languages}")
            st.write(f"**Moneda(s):** {currencies}")

show_country(st.session_state.country)

col1, col2 = st.columns(2)
if col1.button("🎲 Otro país"):
    st.session_state.country = pick_random_country(countries)
    st.rerun()
if col2.button("🔁 Recargar lista (forzar)"):
    load_countries.clear()
    st.rerun()
    
