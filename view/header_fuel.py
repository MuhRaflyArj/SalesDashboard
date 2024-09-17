import streamlit as st
from datetime import date
from pandas import to_datetime
import model.data as data

def header_keseluruhan(df) :
    header_data = {}
    
    col1_1, col1_2 = st.columns([1, 4])

    with col1_1 :
        # Input tanggal awal
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value=date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31), # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data dari pandas dataframe
        header_data["start date"] = to_datetime(header_data["start date"])

        # Input tanggal akhir
        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value=date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        # Mengubah tipe data dari pandas dataframe
        header_data["end date"] = to_datetime(header_data["end date"])

    with col1_2 :
        col1_2_1, col1_2_2 = st.columns([1,2])
        
        with col1_2_1 :
            header_data["selected material"] = st.selectbox(
                "Pilih Material",
                ["Gasoline", "Gasoil"]
            )

            header_data["aggregate"] = st.selectbox(
                "Pilih Agregasi Data",
                ["Mingguan", "Bulanan", "Tahunan"]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"
            elif header_data["aggregate"] == "Tahunan" :
                header_data["aggregate"] = "Y"

        with col1_2_2 :
            if header_data["selected material"] == "Gasoline" :
                header_data["selected bbm"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["PERTALITE", "PERTAMAX", "PERTAMAX TURBO"]
                )

            elif header_data["selected material"] == "Gasoil" :
                header_data["selected bbm"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["BIOSOLAR", "DEXLITE", "PERTAMINA DEX"]
                )

            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume (KL)",
                 "Billing Quantity (KL)", 
                 "Harga Faktur (Rp)", 
                 "Hasil Penjualan (Rp)", 
                 "Margin (Rp)", 
                 "PBBKB (Rp)", 
                 "Net Value (Rp)"]
            )
    
    return header_data

def header_region(df) :
    header_data = {}

    list_region = data.get_list_region(df)
    
    col1_1, col1_2 = st.columns([1, 4])

    with col1_1 :
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value=date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31),
        )

        header_data["start date"] = to_datetime(header_data["start date"])

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value=date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = to_datetime(header_data["end date"])

    with col1_2 :
        col1_2_1, col1_2_2 = st.columns([1,2])
        
        with col1_2_1 :
            header_data["selected material"] = st.selectbox(
                "Pilih Material",
                ["Gasoline", "Gasoil"]
            )

        with col1_2_2 :
            if header_data["selected material"] == "Gasoline" :
                header_data["selected bbm"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["PERTALITE", "PERTAMAX", "PERTAMAX TURBO"]
                )

            elif header_data["selected material"] == "Gasoil" :
                header_data["selected bbm"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["BIOSOLAR", "DEXLITE", "PERTAMINA DEX"]
                )

        col1_2_3, col1_2_4, col1_2_5 = st.columns([2,2,3])

        with col1_2_3 :
            header_data["selected region"] = st.selectbox(
                "Pilih Region",
                list_region
            )
        
        with col1_2_4 :
            header_data["aggregate"] = st.selectbox(
                "Pilih Agregasi Data",
                ["Mingguan", "Bulanan", "Tahunan"]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"
            elif header_data["aggregate"] == "Tahunan" :
                header_data["aggregate"] = "Y"

        with col1_2_5 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume (KL)",
                 "Billing Quantity (KL)", 
                 "Harga Faktur (Rp)", 
                 "Hasil Penjualan (Rp)", 
                 "Margin (Rp)", 
                 "PBBKB (Rp)", 
                 "Net Value (Rp)"]
            )
    
    return header_data

def header_kota(df) :
    header_data = {}

    list_kota = data.get_list_kota(df)
    
    col1_1, col1_2 = st.columns([1, 4])

    with col1_1 :
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value=date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31),
        )

        header_data["start date"] = to_datetime(header_data["start date"])

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value=date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = to_datetime(header_data["end date"])

    with col1_2 :
        header_data["selected kota"] = st.multiselect(
            "Pilih Kabupaten/Kota",
            list_kota
        )

        col1_2_1, col1_2_2 = st.columns([1,1])

        with col1_2_1 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume (KL)",
                 "Billing Quantity (KL)", 
                 "Harga Faktur (Rp)", 
                 "Hasil Penjualan (Rp)", 
                 "Margin (Rp)", 
                 "PBBKB (Rp)", 
                 "Net Value (Rp)"]
            )

        with col1_2_2 :
            header_data["aggregate"] = st.selectbox(
                "Pilih aggregasi data",
                ["Mingguan", "Bulanan", "Tahunan"]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"
            elif header_data["aggregate"] == "Tahunan" :
                header_data["aggregate"] = "Y"

    col2_1, col2_2 = st.columns([1,2])

    with col2_1 :
        header_data["selected material"] = st.selectbox(
            "Pilih Material",
            ["Gasoline", "Gasoil"]
        )

    with col2_2 :
        if header_data["selected material"] == "Gasoline" :
            header_data["selected bbm"] = st.multiselect(
                "Pilih Jenis BBM",
                ["PERTALITE", "PERTAMAX", "PERTAMAX TURBO"]
            )

        elif header_data["selected material"] == "Gasoil" :
            header_data["selected bbm"] = st.multiselect(
                "Pilih Jenis BBM",
                ["BIOSOLAR", "DEXLITE", "PERTAMINA DEX"]
            )

    return header_data