import streamlit as st
import model.data as data
import view.body_fuel as body_fuel
import view.body_lpg as body_lpg
import view.dropdown as dropdown
import view.graph as graph

# COnfigurasi ukuran halaman
st.set_page_config(layout="wide")

# Main title
st.title("Dashboard Penjualan SAM Bandung")

# Dropdown untuk upload file dan 
with st.expander("Upload Data Sales") :
    data_type, uploaded_file = dropdown.upload_popup()

# Tampilan body muncul saat sudah terdapat file yang diupload
if uploaded_file != None :

    # Tampilan untuk dashboard fuel
    if data_type == "Data Fuel" :
        # Baca data excel yang diupload
        df = data.read_data_fuel(uploaded_file)

        # Pilihan jenis visualisasi
        header_option = st.selectbox(
            "Pilih Visualisasi",
            ["Per-SPBU", "Per-Region", "Keseluruhan"]
        )

        # Menampilkan tampilan sesuai jenis visualisasi
        if header_option == "Per-SPBU" :
            body_fuel.body_spbu(df)
        elif header_option == "Per-Region" :
            body_fuel.body_region(df)
        elif header_option == "Keseluruhan" :
            body_fuel.body_keseluruhan(df)

    # Tampilan untuk dashboard LPG
    elif data_type == "Data LPG" :
        # Baca data excel yang diupload
        df = data.read_data_lpg(uploaded_file)
        
        # Pilihan jenis visualisasi
        header_option = st.selectbox(
            "Pilih Visualisasi",
            ["Per-SH", "Per-Region", "Keseluruhan"]
        )

        # Menampilkan tampilan sesuai jenis visualisasi
        if header_option == "Per-SH" :
            body_lpg.body_sh(df)
        elif header_option == "Per-Region" :
            body_lpg.body_region(df)
        elif header_option == "Keseluruhan" :
            body_lpg.body_keseluruhan(df)