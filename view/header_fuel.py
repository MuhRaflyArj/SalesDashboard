import streamlit as st
import model.data as data
from datetime import date
from pandas import to_datetime

# Header jenis visualisasi data per-SPBU
def header_spbu(list_region, dict_lambung, dict_product) :
    # Dictionary untuk menyimpan pilihan yang dipilih user
    header_data = {}

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan Kota dan Lambung
    col1_1, col2_1 = st.columns([2,1])

    # Isi kolom untuk pilihan Kabupaten/Kota
    with col1_1 :
        header_data["selected region"] = st.selectbox(
            "Pilih Kota/Kabupaten",
            list_region # Daftar region didapatkan dari parameter
        )

    # Isi kolom untuk pilihan lambung
    with col2_1 :
        header_data["selected lambung"] = st.selectbox(
            "Pilih No lambung",
            # Daftar lambung sesuai dengan region yang dipilih
            dict_lambung[header_data["selected region"]]
        )

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan tanggal dan
    # informasi lainnya
    col1_2, col2_2 = st.columns([1,4])

    # Isi kolom untuk pilihan tanggal awal dan akhir
    with col1_2:
        # Input tanggal awal
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data ke pandas datetime
        header_data["start date"] = to_datetime(header_data["start date"])

        # Input tanggal akhir
        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data ke pandas datetime
        header_data["end date"] = to_datetime(header_data["end date"])

    # Isi kolom untuk pilihan informasi lainnya
    with col2_2 :
        # Input produk untuk divisualisasikan
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            # Hanya memilih produk yang terdapat pada lambung dipilih
            dict_product[header_data["selected lambung"]]
        )

        # 2 Kolom di dalam kolom informasi lainnya untuk memilih nilai yang ditinjau
        # dan agregasi data
        col2_2_1, col2_2_2 = st.columns(2)

        # Isi untuk kolom pemilihan nilai yang ditinjau
        with col2_2_1 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                # Daftar nilai yang ditinjau
                ["Volume",
                 "Billing Quantity", 
                 "Harga Faktur", 
                 "Hasil Penjualan", 
                 "Margin", 
                 "PBBKB", 
                 "Net Value"]
            )

        # Isi kolom untuk pemilihan agregasi data
        with col2_2_2 :
            header_data["aggregate"] = st.selectbox(
                "Agregasi Data",
                # Pilihan agregasi data
                ["Harian", "Mingguan", "Bulanan",]
            )

            # Konversi agregasi data agar dapat dibaca oleh Pandas Grouper
            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"

    # Mengembalikan data yang dipilih
    return header_data

# Header jenis visualisasi data per-region
def header_region(list_region, dict_product) :
    # Dictionary untuk menyimpan pilihan yang dipilih user
    header_data = {}

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan tanggal
    # dan pemilihan informasi lainnya
    col1_1, col1_2 = st.columns([1,4])

    # Isi kolom untuk pilihan tanggal awal dan akhir
    with col1_1 :
        # Input tanggal awal
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data ke pandas datetime
        header_data["start date"] = to_datetime(header_data["start date"])

        # Input tanggal akhir
        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data ke pandas dataframe
        header_data["end date"] = to_datetime(header_data["end date"])

    # Isi kolom untuk pilihan informasi lainnya
    with col1_2 :
        # Input untuk memilih beberapa region
        header_data["selected region"] = st.multiselect(
            "Pilih Kota/Kabupaten",
            list_region # Daftar region yang dipilih
        )

        # 3 Kolom untuk di dalam informasi lainnya untuk memilih produk, nilai, 
        # dan jenis agregasi data
        col1_2_1, col1_2_2, col1_2_3 = st.columns([2,1,1])

        # Isi kolom untuk memilih produk
        with col1_2_1 :
            # Input untuk memilih beberapa produk
            header_data["selected product"] = st.multiselect(
                "Pilih Produk",
                # Mengambil seluruh jenis produk yang terdapat pada data
                set([j for i in dict_product.values() for j in i if isinstance(j , str)])
            )

        # Isi kolom untuk memilih nilai yang ditinjau
        with col1_2_2 :
            # Input untuk memilih nilai yang ditinjau
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                # Daftar nilai yang ditinjau
                ["Volume",
                 "Billing Quantity", 
                 "Harga Faktur", 
                 "Hasil Penjualan", 
                 "Margin", 
                 "PBBKB", 
                 "Net Value"]
            )

        # Isi kolom untuk pemilihan agregasi data
        with col1_2_3 :
            # Input agregasi data
            header_data["aggregate"] = st.selectbox(
                "Aggregasi Data",
                # Pilihan agregasi data
                ["Harian", "Mingguan", "Bulanan"]
            )

            # Konversi agregasi data agar dapat dibaca oleh Pandas Grouper
            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"

    # Mengembalikan data yang dipilih
    return header_data

# Hedaer jenis visualisai data per-region
def header_keseluruhan(list_product) :
    # Dictionary untuk menyimpan pilihan yang dipilih user
    header_data = {}

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan tanggal
    # dan pemilihan informasi lainnya
    col1_1, col1_2 = st.columns([1,3])
    
    # Isi kolom untuk pilihan tanggal awal dan akhir
    with col1_1 :
        # Input tanggal awal
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        # Mengubah tipe data ke pandas dataframe
        header_data["start date"] = to_datetime(header_data["start date"])

        # Input tanggal akhir
        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        # Mengubah tipe date ke pandas dataframe
        header_data["end date"] = to_datetime(header_data["end date"])

    # Isi kolom untuk pilihan informasi lainnya
    with col1_2 :
        # Input untuk memilih beberapa produk
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            list_product
        )
        
        # 2 Kolom untuk memilih nilai yang ditinjau dan agregat
        col1_2_1, col1_2_2 = st.columns([2,1])
        
        # Isi kolom untuk memilih nilai yang ditinjau
        with col1_2_1 :
            # Input untuk memilih nilai yang ditinjau
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                # Daftar nilai yang ditinjau
                ["Volume",
                 "Billing Quantity", 
                 "Harga Faktur", 
                 "Hasil Penjualan", 
                 "Margin", 
                 "PBBKB", 
                 "Net Value"]
            )

        # Isi kolom untuk pemilihan agregasi data
        with col1_2_2 :
            # Input agregasi data
            header_data["aggregate"] = st.selectbox(
                "Aggreagasi Data",
                # Pilihan agregasi data
                ["Harian", "Mingguan", "Bulanan"]
            )

            # Konversi agregasi data agar dapat dibaca oleh Pandas Grouper
            if header_data["aggregate"] == "Harian" :
                header_data["aggregate"] = "D"
            elif header_data["aggregate"] == "Mingguan" :
                header_data["aggregate"] = "W"
            elif header_data["aggregate"] == "Bulanan" :
                header_data["aggregate"] = "M"

    # Mengembalikan data yang dipilih
    return header_data

def header_mingguan() :
    header_data = {}

    col1_1, col1_2 = st.columns([1, 3])

    with col1_1 :
        header_data["start date"] = st.date_input(
            "Pilih Tanggal Awal",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(),
            min_value = date(2000, 1, 1),
            max_value = date(2030, 12, 31)
        )

    with col1_2 :
        header_data["selected fueltype"] = st.selectbox(
            "Pilih Tipe BBM",
            ["Bensin", "Solar"]
        )

        col1_1_1, col1_1_2 = st.columns([2,1])

        with col1_1_1 :
            if header_data["selected fueltype"] == "Bensin" :
                header_data["selected product"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["Pertalite", "Pertamax", "Pertamax Green", "Pertamax Turbo"]
                )
            elif header_data["selected fueltype"] == "Solar" :
                header_data["selected product"] = st.multiselect(
                    "Pilih Jenis BBM",
                    ["Biosolar", "Dex", "Dexlite"]
                )

        with col1_1_2 :
            header_data["selected value"] = st.selectbox(
                "Pilih Nilai yang Ditinjau",
                ["Volume",
                 "Billing Quantity", 
                 "Harga Faktur", 
                 "Hasil Penjualan", 
                 "Margin", 
                 "PBBKB", 
                 "Net Value"]
            )

    return header_data
        