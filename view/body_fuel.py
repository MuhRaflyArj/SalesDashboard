import streamlit as st
import view.graph as graph
import model.data as data

def body_keseluruhan(df, header_data) :
    proportion_data = data.get_proporsi_keseluruhan(df, header_data)

    barchart_porporsi = graph.barchart_proporsi(proportion_data, header_data)
    st.plotly_chart(barchart_porporsi)
    print(proportion_data)
    
    st.write("Body Keseluruhan")

def body_region(df, header_data) :
    st.write("Body Region")

def body_kota(df, header_data) :
    st.write("Body Kota")