import pandas as pd
import plotly.graph_objects as go
import streamlit as st

@st.cache_data
def read_data_fuel(uploaded_file) :
    df = pd.read_excel(uploaded_file, sheet_name="target", skiprows=4)
    
    df.columns = list(df.columns.values[:-9]) + ["Material Code", "Material Name", "Billing Quantity (KL)", "Volume (KL)", "Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]
    df["Material Name"] = df["Material Name"].str.replace(", ", "",).str.replace(",", "",).str.replace("BULK", "",)

    df[["Billing Quantity (KL)", "Volume (KL)", "Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]] = df[["Billing Quantity (KL)", "Volume (KL)", "Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]].fillna(0)
    df = df.dropna(subset=[
        "Calendar Day",
        "Region",
        "Sales District",
        "No Lambung",
        "Material Name",
        "Material Code"
    ])

    fuel_names = {
        'PERTALITE': 'PERTALITE', 
        'PERTAMAX': 'PERTAMAX', 
        'PERTAMAX TURBO': 'PERTAMAX TURBO', 
        'PERTAMAX GREEN': 'PERTAMAX GREEN', 
        'BIOSOLAR B30': 'BIOSOLAR', 
        'BIOSOLAR B35': 'BIOSOLAR', 
        'DEXLITE': 'DEXLITE', 
        'PERTAMINA DEX 50 PPM': 'PERTAMINA DEX'
    }

    df["Material Name"] = df["Material Name"].replace(fuel_names)

    df["Margin (Rp)"] = abs(df["Margin (Rp)"])
    
    return df

def get_list_kota(df) :
    return list(df["Sales District"].unique())

def get_list_region(df) :
    return list(df["Region"].unique())

def get_proporsi_produk_keseluruhan(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    data = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), 
            "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    return data

def get_proporsi_produk_region(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Region"] == header_data["selected region"]) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    data = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), 
            "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    return data

def get_proporsi_produk_kota(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Sales District"].isin(header_data["selected kota"])) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    data = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), 
            "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    return data

def get_proporsi_sales_keseluruhan(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Calendar Day"] >= header_data["pie start date"]) &
        (df["Calendar Day"] <= header_data["pie end date"])
    ][["Material Name", header_data["selected value"]]]

    data = data.groupby(["Material Name"])

    return data

def get_proporsi_sales_region(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Region"] == header_data["pie selected region"]) &
        (df["Calendar Day"] >= header_data["pie start date"]) &
        (df["Calendar Day"] <= header_data["pie end date"])
    ][["Material Name", header_data["selected value"]]]

    data = data.groupby(["Material Name"])

    return data

def get_proporsi_sales_kota(df, header_data) :
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Sales District"] == header_data["pie selected kota"]) &
        (df["Calendar Day"] >= header_data["pie start date"]) &
        (df["Calendar Day"] <= header_data["pie end date"])
    ][["Material Name", header_data["selected value"]]]

    data = data.groupby(["Material Name"])

    return data
    
def get_total_pencapaian_keseluruhan(df, header_data) :
    data = {}

    for material in header_data["selected type"] :
        data[material] = df.loc[
            (df["Calendar Day"] >= header_data["start date"]) &
            (df["Calendar Day"] <= header_data["end date"]) &
            (df["Material Name"] == material)
        ][header_data["selected value"]].sum()

    return data

def get_total_pencapaian_region(df, header_data) :
    data = {}

    for material in header_data["selected type"] :
        data[material] = df.loc[
            (df["Calendar Day"] >= header_data["start date"]) &
            (df["Calendar Day"] <= header_data["end date"]) &
            (df["Material Name"] == material) &
            (df["Region"] == header_data["selected region"])
        ][header_data["selected value"]].sum()

    return data

def get_total_pencapaian_kota(df, header_data) :
    data = {}

    for material in header_data["selected type"] :
        data[material] = df.loc[
            df
        ]

def get_rata_rata_keselurhan(df, header_data):
    # Filter data berdasarkan material yang dipilih dan rentang tanggal
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    # Jika data kosong, kembalikan DataFrame kosong dengan kolom yang diharapkan
    if data.empty:
        return pd.DataFrame(columns=["Calendar Day", "Material Name", "Rerata"])

    # Agregasikan data per bulan
    data_bulanan = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    # Buat kolom baru yang menghitung jumlah hari dalam setiap bulan
    data_bulanan["days_in_month"] = data_bulanan["Calendar Day"].apply(
        lambda x: pd.date_range(start=x.replace(day=1), end=x).size
    )

    # Hitung rata-rata penjualan harian
    data_bulanan["Rerata"] = (
        data_bulanan[header_data["selected value"]] / data_bulanan["days_in_month"]
    )

    return data_bulanan[["Calendar Day", "Material Name", "Rerata"]]

def get_rata_rata_region(df, header_data) :
    # Filter data berdasarkan material yang dipilih dan rentang tanggal
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Region"] == header_data["selected region"]) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    # Jika data kosong, kembalikan DataFrame kosong dengan kolom yang diharapkan
    if data.empty:
        return pd.DataFrame(columns=["Calendar Day", "Material Name", "Rerata"])

    # Agregasikan data per bulan
    data_bulanan = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    # Buat kolom baru yang menghitung jumlah hari dalam setiap bulan
    data_bulanan["days_in_month"] = data_bulanan["Calendar Day"].apply(
        lambda x: pd.date_range(start=x.replace(day=1), end=x).size
    )

    # Hitung rata-rata penjualan harian
    data_bulanan["Rerata"] = (
        data_bulanan[header_data["selected value"]] / data_bulanan["days_in_month"]
    )

    return data_bulanan[["Calendar Day", "Material Name", "Rerata"]]


def get_rata_rata_kota(df, header_data) :
    # Filter data berdasarkan material yang dipilih dan rentang tanggal
    data = df.loc[
        (df["Material Name"].isin(header_data["selected type"])) &
        (df["Sales District"].isin(header_data["selected kota"])) &
        (df["Calendar Day"] >= header_data["start date"]) &
        (df["Calendar Day"] <= header_data["end date"])
    ]

    # Jika data kosong, kembalikan DataFrame kosong dengan kolom yang diharapkan
    if data.empty:
        return pd.DataFrame(columns=["Calendar Day", "Material Name", "Rerata"])

    # Agregasikan data per bulan
    data_bulanan = (
        data.groupby(
            [pd.Grouper(key="Calendar Day", freq=header_data["aggregate"]), "Material Name"]
        )[header_data["selected value"]]
        .sum()
        .reset_index()
    )

    # Buat kolom baru yang menghitung jumlah hari dalam setiap bulan
    data_bulanan["days_in_month"] = data_bulanan["Calendar Day"].apply(
        lambda x: pd.date_range(start=x.replace(day=1), end=x).size
    )

    # Hitung rata-rata penjualan harian
    data_bulanan["Rerata"] = (
        data_bulanan[header_data["selected value"]] / data_bulanan["days_in_month"]
    )

    return data_bulanan[["Calendar Day", "Material Name", "Rerata"]]


# ==================================================== #

@st.cache_data
def read_data_lpg(uploaded_file) :
    df = pd.read_excel(uploaded_file, sheet_name="target", skiprows=4)
    df.columns = list(df.columns.values[:-8]) + ["Material Code", "Material Name", "Billing Quantity (MT)", "Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]
    
    df[["Billing Quantity (KL)","Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]] = df[["Billing Quantity (MT)", "Harga Faktur (Rp)", "Hasil Penjualan (Rp)", "Margin (Rp)", "PBBKB (Rp)", "Net Value (Rp)"]].fillna(0)
    df = df.dropna(subset=[
        "Calendar Day",
        "Region",
        "Sales District",
        "SH Name",
        "Material Name",
        "Material Code"
    ])

    lpg_names ={
        "LPG MIXED,BULK" : "BULK",
        "TABUNG LPG\xa0 BARU @50KG BAJA" : "LPG NPSO 50 KG",
        "TABUNG LPG\xa0 BARU @3KG BAJA" : "LPG PSO 3 KG",
        "REFILL/ISI LPG @3KG (NET)" : "LPG PSO 3 KG",
        "TABUNG BARU BRIGHT GAS @5.5 KG" : "LPG NPSO 5,5 KG",
        "TABUNG + ISI BRIGHT GAS @12KG BAJA" : "LPG NPSO 12 KG",
        "TABUNG BRIGHT GAS BARU @12KG BAJA" : "LPG NPSO 12 KG",
        "LPG BRIGHT GAS 5.5KG (NET)" : "LPG NPSO 5,5 KG",
        "REFILL/ISI LPG @12KG (NET)" : "LPG NPSO 12 KG",
        "TABUNG + ISI LPG @3KG BAJA" : "LPG PSO 3 KG",
        "TABUNG + ISI LPG @50KG BAJA" : "LPG NPSO 50 KG",
        "BRIGHT GAS, CAN @220GR" : "BG Can",
        "TABUNG + ISI LPG @12KG BAJA" : "LPG NPSO 12 KG",
        "TABUNG LPG\xa0 BARU @12KG BAJA" : "LPG NPSO 12 KG",
        "TABUNG + ISI BRIGHT GAS @5.5KG BAJA" : "LPG NPSO 5,5 KG",
        "REFILL/ISI LPG @50KG (NET)" : "LPG NPSO 50 KG",
    }
    
    df["Material Name"] = df["Material Name"].replace(lpg_names)

    df["Margin (Rp)"] = abs(df["Margin (Rp)"])

    return df