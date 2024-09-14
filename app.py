import streamlit as st
import model.data as data
import view.body_fuel as body_fuel
import view.body_lpg as body_lpg
import view.header_fuel as header
import view.graph as graph


# Configurasi ukuran halaman
st.set_page_config(layout="wide")

# Judul utama
st.title("Dashboard Penjualan SAM Bandung")

tab_profile, tab_fuel, tab_sales = st.tabs(["Profil Bisnis", "Fuel Sales", "Gas Sales"])


with tab_fuel :
    fuel_data = st.file_uploader("Pastikan nama sheet adalah `target`", type="xlsx")
    
    if fuel_data != None :
        fuel_df = data.read_data_fuel(fuel_data)

        st.divider()

        visualization_type = st.selectbox(
            "Pilih jenis visualisasi",
            ["Keseluruhan Data", "Per-Region", "Per-Kabupaten/Kota"]
        )

        if visualization_type == "Keseluruhan Data" :
            header_data = header.header_keseluruhan(fuel_df)
        elif visualization_type == "Per-Region" :
            header_data = header.header_region(fuel_df)
        elif visualization_type == "Per-Kabupaten/Kota" :
            header_data = header.header_kota(fuel_df)

        st.divider()

        if visualization_type == "Keseluruhan Data" :
            body_fuel.body_keseluruhan(fuel_df, header_data)
        elif visualization_type == "Per-Region" :
            body_fuel.body_region(fuel_df, header_data)
        elif visualization_type == "Per-Kabupaten/Kota" :
            body_fuel.body_kota(fuel_df, header_data)