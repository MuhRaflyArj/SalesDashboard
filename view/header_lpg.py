import streamlit as st
from datetime import date
from pandas import to_datetime

# Header jenis visualisasi data per-SH
def header_sh(list_region, dict_sh, dict_product) :
    # Dictionary untuk menyimpan pilihan yang dipilih user
    header_data = {}

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan Kota dan Lambung
    col1_1, col1_2 = st.columns([2, 1])

    # Isi kolom untuk memilih region
    with col1_1 :
        # Pilihan untuk memilih region
        selected_region = st.selectbox(
            "Pilih Kota/Kabupaten",
            list_region # Daftar region yang didapatkan dari parameter
        )

    # Isi kolom untuk memilih SH
    with col1_2 :
        # Input untuk memilih SH
        header_data["selected sh"] = st.selectbox(
            "Pilih SH",
            # Daftar SH sesuai dengan region yang dipilih
            dict_sh[selected_region]
        )

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan tanggal dan
    # informasi lainnya
    col2_1, col2_2 = st.columns([1,4])

    # Isi kolom untuk pilihan tanggal awal dan akhir
    with col2_1 :
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

    # Isi kolom untuk pilihan produk, nilai yang ditinjau
    # dan agregasi data
    with col2_2 :
        # Input produk untuk divisualisasikan
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            # Hanya memilih produk yang terdapat pada lambung dipilih
            dict_product[header_data["selected sh"]]
        )

        # 2 kolom di dalam kolom informasi lainnya untuk memilih nilai yang ditinjau
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
            # Pilihan untuk agregasi data
            header_data["aggregate"] = st.selectbox(
                "Agreagasi Data",
                # Pilihan agregasi data
                ["Harian", "Mingguan", "Bulanan"]
            )

            # Konversi agregasi data dapat dibaca oleh Pandas Grouper
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
            min_value = date(2000, 1, 1), # Nilai minimun yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe data ke pandas dataframe
        header_data["start date"] = to_datetime(header_data["start date"])

        # Input tanggal akhir
        header_data["end date"] = st.date_input(
            "Pilih Tanggal Akhir",
            value = date.today(), # Default value hari ini
            min_value = date(2000, 1, 1), # Nilai minimum yang dapat diinput
            max_value = date(2030, 12, 31) # Nilai maksimum yang dapat diinput
        )

        # Mengubah tipe date ke pandas dataframe
        header_data["end date"] = to_datetime(header_data["end date"])

    # Isi kolom untuk pilihan informasi lainnya
    with col1_2 :
        # Input untuk memilih beberapa region
        header_data["selected region"] = st.multiselect(
            "Pilih Kota/Kabupaten",
            list_region # Daftar region yang dipilih
        )

        # 3 Kolom untuk di dalam informasi lainnya untuk memilih produk, nilai
        # dan jenis agregasi data
        col1_2_1, col1_2_2, col1_2_3  = st.columns([2,1,1])

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
            # Input untuk memilih yang ditinjau
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
                #  Pilihan agregasi data
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

# Header jenis visualisasi data keseluruhan
def header_keseluruhan(list_product) :
    # Dictionary untuk menyimpan pilihan yang dipilih user
    header_data = {}

    # ========================= #
    # 2 Kolom pada baris pertama untuk pemilihan tanggal
    # dan pemilihan informasi lainnya
    col1_1, col1_2 = st.columns([1, 3])

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

        # Menghubah tipe data ke pandas dataframe
        header_data["end date"] = to_datetime(header_data["end date"])

    # Isi kolom untuk informasi lainnya
    with col1_2 :
        # Input untuk memilih beberapa produk
        header_data["selected product"] = st.multiselect(
            "Pilih Produk",
            list_product # Daftar produk yang dapat dipilih
        )

        # 2 Kolom di dalam informasi lainnya untuk memilik nilai
        # dan jenis agregasi data 
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
