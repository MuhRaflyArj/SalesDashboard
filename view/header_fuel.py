import streamlit as st
import model.data as data
from datetime import date
from pandas import to_datetime

def header_spbu(list_region, dict_lambung, dict_product) :
    header_data = {}
    col1_1, col2_1 = st.columns([2,1])

    with col1_1 :
        selected_region = st.selectbox(
            "Pilih Kota/Kabupaten",
            list_region
        )

    with col2_1 :

        header_data["selected lambung"] = st.selectbox(
            "Pilih No lambung",
            dict_lambung[selected_region]
        )

    col1_2, col2_2 = st.columns([1,4])

    with col1_2:
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["start date"] = to_datetime(header_data["start date"])

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = to_datetime(header_data["end date"])

    with col2_2 :
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            dict_product[header_data["selected lambung"]]
        )

        col2_2_1, col2_2_2 = st.columns(2)

        with col2_2_1 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume", "Billing Quantity", "Harga Faktur", "Hasil Penjualan", "Margin", "PBBKB", "Net Value"]
            )

        with col2_2_2 :
            header_data["aggregate"] = st.selectbox(
                "Agregasi Data",
                ["Harian", "Mingguan", "Bulanan",]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"

    return header_data

def header_region(list_region, dict_product) :
    header_data = {}
    col1_1, col1_2 = st.columns([1,4])

    with col1_1 :
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["start date"] = to_datetime(header_data["start date"])

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = to_datetime(header_data["end date"])
    
    with col1_2 :
        header_data["selected region"] = st.multiselect(
            "Pilih Kota/Kabupaten",
            list_region
        )

        col1_2_1, col1_2_2, col1_2_3 = st.columns([2,1,1])

        with col1_2_1 :
            header_data["selected product"] = st.multiselect(
                "Pilih Produk",
                set([j for i in dict_product.values() for j in i if isinstance(j , str)])
            )

        with col1_2_2 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume", "Harga Faktur", "Hasil Penjualan", "Margin", "PBBKB", "Net Value"]
            )

        with col1_2_3 :
            header_data["aggregate"] = st.selectbox(
                "Aggregasi Data",
                ["Harian", "Mingguan", "Bulanan"]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"


    return header_data

def header_keseluruhan(list_product) :
    header_data = {}

    col1_1, col1_2 = st.columns([1,3])

    with col1_1 :
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["start date"] = to_datetime(header_data["start date"])

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = to_datetime(header_data["end date"])

    with col1_2 :
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            list_product
        )

        col1_2_1, col1_2_2 = st.columns([2,1])
        
        with col1_2_1 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume", "Harga Faktur", "Hasil Penjualan", "Margin", "PBBKB", "Net Value"]
            )

        with col1_2_2 :
            header_data["aggregate"] = st.selectbox(
                "Aggreagasi Data",
                ["Harian", "Mingguan", "Bulanan"]
            )

            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"

    return header_data