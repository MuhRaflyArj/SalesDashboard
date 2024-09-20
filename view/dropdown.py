import pandas as pd
import streamlit as st

def preview_data_fuel(df) :
    cols = st.columns(5)

    with cols[0] :
        n_start = st.number_input("Awal Baris", step=1, value=0, format="%d")
    with cols[1] :
        n_end = st.number_input("Akhir Baris", step=1, value=100, format="%d")

    st.dataframe(df.iloc[n_start:n_end], use_container_width=True)

def preview_data_lpg(df) :
    cols = st.columns(5)

    with cols[0] :
        n_start = st.number_input("Awal Baris ", step=1, value=0, format="%d")
    with cols[1] :
        n_end = st.number_input("Akhir Baris ", step=1, value=100, format="%d")

    st.dataframe(df.iloc[n_start:n_end], use_container_width=True)



def panduan(df) :
    pass