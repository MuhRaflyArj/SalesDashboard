import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

@st.cache_data
def read_data_fuel(uploaded_file) :
    df = pd.read_excel(uploaded_file, sheet_name="target", skiprows=4)
    df.columns = list(df.columns.values[:-9]) + ["Material Code", "Material Name", "Billing Quantity", "Volume", "Harga Faktur", "Hasil Penjualan", "Margin", "PBBKB", "Net Value"]
    df["Material Name"] = df["Material Name"].str.replace(", ", "",).str.replace(",", "",).str.replace("BULK", "",)
    return df

@st.cache_data
def read_data_lpg(uploaded_file) :
    df = pd.read_excel(uploaded_file, sheet_name="target", skiprows=4)
    df.columns = list(df.columns.values[:-8]) + ["Material Code", "Material Name", "Billing Quantity", "Harga Faktur", "Hasil Penjualan", "Margin", "PBBKB", "Net Value"]
    
    return df

def get_region_names(df) :
    return list(df["Sales District"].unique())

def get_no_lambung(df) :
    region_names = get_region_names(df)

    dict_lambung = {
        region : sorted(list(df.loc[df["Sales District"] == region]["No Lambung"].unique())) for region in region_names
    }

    return dict_lambung

def get_sh_names(df) :
    region_names = get_region_names(df)

    dict_sh = {
        region: sorted(list(df.loc[df["Sales District"] == region]["SH Name"].unique())) for region in region_names
    }

    return dict_sh

def get_sales_data_sh(df, sh, num_col, start_date, end_date, aggregate='M') :
    data = df.loc[
        (df["SH Name"] == sh) &
        (df["Calendar Day"] >= start_date) &
        (df["Calendar Day"] <= end_date)
    ]

    data = (
        data.groupby([pd.Grouper(key="Calendar Day", freq=aggregate), 'Material Name'])[num_col]
        .sum()
        .reset_index()
    )

    return data

def get_sales_data_spbu(df, lambung, num_col, start_date, end_date, aggregate='M') :

    data = df.loc[
        (df["No Lambung"] == lambung) & 
        (df["Calendar Day"] >= start_date) & 
        (df["Calendar Day"] <= end_date)
    ]

    # Group by Calendar Day and Material Name and aggregate
    data = (
        data.groupby([pd.Grouper(key="Calendar Day", freq=aggregate), 'Material Name'])[num_col]
        .sum()
        .reset_index()
    )

    return data

def get_sales_data_region(df, regions, products, num_col, start_date, end_date, aggregate='M') :
    data = df.loc[
        (df["Sales District"].isin(regions)) &
        (df["Material Name"].isin(products)) &
        (df["Calendar Day"] >= start_date) &
        (df["Calendar Day"] <= end_date)
    ]

    data = (
        data.groupby([pd.Grouper(key="Calendar Day", freq=aggregate), "Sales District"])[num_col]
        .sum()
        .reset_index()
    )

    return data

def get_sales_data_keseluruhan(df, products, num_col, start_date, end_date, aggregate="M") :
    data = df.loc[
        (df["Material Name"].isin(products)) &
        (df["Calendar Day"] >= start_date) &
        (df["Calendar Day"] <= end_date)
    ]

    data = (
        data.groupby([pd.Grouper(key="Calendar Day", freq=aggregate), "Material Name"])[num_col]
        .sum()
        .reset_index()
    )

    return data

def get_header_data_spbu(df) :
    list_region = get_region_names(df)
    dict_lambung = get_no_lambung(df)
    dict_product = get_product_spbu(df)

    return list_region, dict_lambung, dict_product

def get_header_data_sh(df) :
    list_region = get_region_names(df)
    dict_sh = get_sh_names(df)
    dict_product = get_product_sh(df)

    return list_region, dict_sh, dict_product

def get_header_data_region(df) :
    list_region = get_region_names(df)
    dict_product = get_product_region(df)

    return list_region, dict_product

def get_header_data_keseluruhan(df) :
    list_product = get_product_keseluruhan(df)

    return list_product

def get_product_spbu(df) :
    dict_lambung = get_no_lambung(df)
    dict_product = {}

    for daftar_lambung in dict_lambung.values() :
        for lambung in daftar_lambung:
            dict_product[lambung] = list(df.loc[df["No Lambung"] == lambung]["Material Name"].unique())

    return dict_product

def get_product_sh(df) :
    dict_sh = get_sh_names(df)
    dict_product = {}

    for daftar_sh in dict_sh.values() :
        for sh in daftar_sh :
            dict_product[sh] = list(df.loc[df["SH Name"] == sh]["Material Name"].unique())

    return dict_product

def get_product_region(df) :
    list_region = get_region_names(df)
    dict_product = {}

    for region in list_region :
        dict_product[region] = list(df.loc[df["Sales District"] == region]["Material Name"].unique())

    return dict_product

def get_product_keseluruhan(df) :
    return list(df["Material Name"].unique())

def get_total_sales_sh(df, sh, products, value, start_date, end_date) :
    total_sales_dict = {}

    for product in products :
        total = df.loc[
            (df["SH Name"] == sh) &
            (df["Material Name"] == product) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        total_sales_dict[product] = total
    
    return total_sales_dict

def get_total_sales_spbu(df, lambung, products, value, start_date, end_date) :
    total_sales_dict = {}

    for product in products :
        total = df.loc[
            (df["No Lambung"] == lambung) &
            (df["Material Name"] == product) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        total_sales_dict[product] = total

    return total_sales_dict

def get_total_pso_sh(df, sh, value, start_date, end_date) :
    total_pso = {}

    for type in list(df["Price List Type"].unique()) :
        total = df.loc[
            (df["SH Name"] == sh) &
            (df["Price List Type"] == type) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        total_pso[type] = total

    return total_pso

def get_total_pso_spbu(df, lambung, value, start_date, end_date) :
    total_pso = {}

    for type in list(df["Price List Type"].unique()) :
        total = df.loc[
            (df["No Lambung"] == lambung) &
            (df["Price List Type"] == type) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        total_pso[type] = total

    return total_pso

def get_total_pso_region(df, regions, value, start_date, end_date) :
    total_pso = {}

    for product in list(df["Price List Type"].unique()) :
        total_pso[product] = 0
        for region in regions :
            total = df.loc[
                (df["Sales District"] == region) &
                (df["Price List Type"] == product) &
                (df["Calendar Day"] >= start_date) &
                (df["Calendar Day"] <= end_date)
            ][value].sum()

            total_pso[product] += total

    return total_pso

def get_total_pso_keseluruhan(df, value, start_date, end_date) :
    total_pso = {}

    for product in list(df["Price List Type"].unique()) :
        total = df.loc[
            (df["Price List Type"] == product) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        total_pso[product] = total

    return total_pso
 
def get_sum_region(df, regions, products, value, start_date, end_date) :
    region_sales = {}

    for region in regions :
        region_sales[region] = {}
        for product in products :
            total = df.loc[
                (df["Sales District"] == region) &
                (df["Material Name"] == product) &
                (df["Calendar Day"] >= start_date) &
                (df["Calendar Day"] <= end_date)
            ][value].sum()

            region_sales[region][product] = total

    return region_sales

def get_sum_keseluruhan(df, products, value, start_date, end_date) :
    keseluruhan_sales = {}

    for product in products :
        total = df.loc[
            (df["Material Name"] == product) &
            (df["Calendar Day"] >= start_date) &
            (df["Calendar Day"] <= end_date)
        ][value].sum()

        keseluruhan_sales[product] = total

    return keseluruhan_sales


