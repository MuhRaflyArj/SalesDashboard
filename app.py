import streamlit as st
import model.data as data
import view.body_fuel as body_fuel
import view.body_lpg as body_lpg
import view.header_fuel as header_fuel
import view.header_lpg as header_lpg
import view.graph as graph


# Configurasi ukuran halaman
st.set_page_config(layout="wide")

# Judul utama
st.title("Dashboard Penjualan SAM Bandung")

tab_profile, tab_fuel, tab_lpg = st.tabs(["Profil Bisnis", "Fuel Sales", "Gas Sales"])


with tab_fuel :
    with st.expander("Panduan") :
            st.write("Panduan")

    fuel_data = st.file_uploader("Pastikan nama sheet adalah `target`", type="xlsx")

    with st.expander("Preview Data") :
        if fuel_data == None :
            st.write("Data tidak dapat terbaca")
        else :
            st.dataframe(fuel_data.head(), use_container_width=True)

    if fuel_data != None :
        fuel_df = data.read_data_fuel(fuel_data)

        st.divider()

        visualization_type = st.selectbox(
            "Pilih jenis visualisasi",
            ["Keseluruhan Data", "Per-Region", "Per-Kabupaten/Kota"]
        )

        if visualization_type == "Keseluruhan Data" :
            header_data = header_fuel.header_keseluruhan(fuel_df)
        elif visualization_type == "Per-Region" :
            header_data = header_fuel.header_region(fuel_df)
        elif visualization_type == "Per-Kabupaten/Kota" :
            header_data = header_fuel.header_kota(fuel_df)

        st.divider()

        if visualization_type == "Keseluruhan Data" :
            body_fuel.body_keseluruhan(fuel_df, header_data)
        elif visualization_type == "Per-Region" :
            body_fuel.body_region(fuel_df, header_data)
        elif visualization_type == "Per-Kabupaten/Kota" :
            body_fuel.body_kota(fuel_df, header_data)

    with tab_lpg :
        with st.expander("Panduan") :
            st.write("Panduan")

        lpg_data = st.file_uploader("Pastikan nama sheet adalah `target` ", type="xlsx")  

        if lpg_data != None :
            lpg_df = data.read_data_lpg(lpg_data)

            with st.expander("Preview Data") :
                cols = st.columns(5)

                with cols[0] :
                    n_start = st.number_input("Awal", step=1, value=0, format="%d")
                with cols[1] :
                    n_end = st.number_input("Akhir", step=1, value=100, format="%d")

                st.dataframe(lpg_df.iloc[n_start:n_end], use_container_width=True)

            st.divider()

            visualization_type = st.selectbox(
                "Pilih jenis visualisasi ",
                ["Keseluruhan Data", "Per-Region", "Per-Kabupaten/Kota"]
            )

            if visualization_type == "Keseluruhan Data" :
                header_data = header_lpg.header_keseluruhan(lpg_df)
            elif visualization_type == "Per-Region" :
                header_data = header_lpg.header_region(lpg_df)
            elif visualization_type == "Per-Kabupaten/Kota" :
                header_data = header_lpg.header_kota(lpg_df)

            st.divider()

            if visualization_type == "Keseluruhan Data" :
                body_lpg.body_keseluruhan(lpg_df, header_data)
            elif visualization_type == "Per-Region" :
                body_lpg.body_region(lpg_df, header_data)
            elif visualization_type == "Per-Kabupaten/Kota" :
                body_lpg.body_kota(lpg_df, header_data)