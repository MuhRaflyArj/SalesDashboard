import streamlit as st
import view.graph as graph
import model.data as data
from pandas import to_datetime
import pandas as pd
import view.style as style

def body_keseluruhan(df, header_data) :
    proportion_data = data.get_proporsi_produk_keseluruhan(df, header_data)

    barchart_porporsi = graph.barchart_proporsi(proportion_data, header_data)
    st.plotly_chart(barchart_porporsi, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns([3,5])

    with col1 :
        data_realisasi = data.get_total_pencapaian_keseluruhan(df, header_data)
       # Initialize an empty table or with some default values
        df_realisasi ={
            "Material": data_realisasi.keys(),
            "Target": [0.0 for i in range(len(header_data["selected type"]))],
            "Target YTD": [0.0 for i in range(len(header_data["selected type"]))],
            "Real YTD": data_realisasi.values(),
            "%": [0.0 for i in range(len(header_data["selected type"]))],
        }

        df_realisasi = pd.DataFrame(df_realisasi)

        with st.expander("Input Data Target") :
            # Display editable table for "Target" and "Target YTD" input
            input_realisasi = st.data_editor(df_realisasi[["Material", "Target", "Target YTD"]], num_rows="static", use_container_width=True)
        
        df_realisasi["Target"] = input_realisasi["Target"]
        df_realisasi["Target YTD"] = input_realisasi["Target YTD"]
        df_realisasi["%"] = (df_realisasi["Real YTD"] / input_realisasi["Target YTD"]) * 100

        # Apply icons to the percentage column
        df_realisasi["%"] = df_realisasi["%"].apply(lambda x: style.status_icon(x))

        total_row = {
            "Material": "Total",
            "Target": df_realisasi["Target"].sum(),
            "Target YTD": df_realisasi["Target YTD"].sum(),
            "Real YTD": df_realisasi["Real YTD"].sum(),
            "%": style.status_icon(df_realisasi["%"].apply(lambda x: float(x.split()[1][:-1].replace(",", ""))).mean())  # Average of percentage values
        }

        # Create a DataFrame for the total row
        total_row_df = pd.DataFrame([total_row])

        # Concatenate the total row to the original DataFrame
        df_realisasi = pd.concat([df_realisasi, total_row_df], ignore_index=True)

        df_realisasi.reset_index(drop=True, inplace=True)

        # Format numbers as currency and percentages
        df_styled = df_realisasi.style.format({
            "Target": "{:,.2f}",
            "Target YTD": "{:,.0f}",
            "Real YTD": "{:,.2f}",
        }).apply(style.highlight_total_row, axis=1)  # Hide the index
        
        # Define the style for table elements
        df_styled = df_styled.set_properties(**{
            'text-align': 'center', 'font-weight': 'bold', 'border': '1px solid black'
        })
        
        # Display the DataFrame using Streamlit
        st.dataframe(df_styled, use_container_width=True, hide_index=True)

    with col2 :
        col1_1, _, col1_2 = st.columns([7,1,7])

        with col1_1 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])

            pie_data_left = data.get_proporsi_sales_keseluruhan(
                df,
                header_data,
            )
            piechart_proporsi_left = graph.piechart_proporsi(pie_data_left.sum(), header_data, category="keseluruhan")

            st.plotly_chart(piechart_proporsi_left, use_container_width=True)
        
        with col1_2 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal ",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir ",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])

            pie_data_right = data.get_proporsi_sales_keseluruhan(
                df, 
                header_data,
            )
            piechart_proporsi_right = graph.piechart_proporsi(pie_data_right.sum(), header_data, "keseluruhan")

            st.plotly_chart(piechart_proporsi_right, use_container_width=True)

    st.divider()

    data_rerata = data.get_rata_rata_keselurhan(df, header_data)
    linechart_rerata = graph.linechart_rerata(data_rerata, header_data)
    st.plotly_chart(linechart_rerata, use_column_width=True)
    


def body_region(df, header_data) :
    proportion_data = data.get_proporsi_produk_region(df, header_data)

    barchart_porporsi = graph.barchart_proporsi(proportion_data, header_data)
    st.plotly_chart(barchart_porporsi, use_container_width=True)

    st.divider()

    col1, col2 = st.columns([3,5])

    with col1 :
        data_realisasi = data.get_total_pencapaian_keseluruhan(df, header_data)
       # Initialize an empty table or with some default values
        df_realisasi ={
            "Material": data_realisasi.keys(),
            "Target": [0.0 for i in range(len(header_data["selected type"]))],
            "Target YTD": [0.0 for i in range(len(header_data["selected type"]))],
            "Real YTD": data_realisasi.values(),
            "%": [0.0 for i in range(len(header_data["selected type"]))],
        }

        df_realisasi = pd.DataFrame(df_realisasi)

        with st.expander("Input Data Target") :
            # Display editable table for "Target" and "Target YTD" input
            input_realisasi = st.data_editor(df_realisasi[["Material", "Target", "Target YTD"]], num_rows="static", use_container_width=True)
        
        df_realisasi["Target"] = input_realisasi["Target"]
        df_realisasi["Target YTD"] = input_realisasi["Target YTD"]
        df_realisasi["%"] = (df_realisasi["Real YTD"] / input_realisasi["Target YTD"]) * 100

        # Apply icons to the percentage column
        df_realisasi["%"] = df_realisasi["%"].apply(lambda x: style.status_icon(x))

        total_row = {
            "Material": "Total",
            "Target": df_realisasi["Target"].sum(),
            "Target YTD": df_realisasi["Target YTD"].sum(),
            "Real YTD": df_realisasi["Real YTD"].sum(),
            "%": style.status_icon(df_realisasi["%"].apply(lambda x: float(x.split()[1][:-1].replace(",", ""))).mean())  # Average of percentage values
        }

        # Create a DataFrame for the total row
        total_row_df = pd.DataFrame([total_row])

        # Concatenate the total row to the original DataFrame
        df_realisasi = pd.concat([df_realisasi, total_row_df], ignore_index=True)

        df_realisasi.reset_index(drop=True, inplace=True)

        # Format numbers as currency and percentages
        df_styled = df_realisasi.style.format({
            "Target": "{:,.2f}",
            "Target YTD": "{:,.0f}",
            "Real YTD": "{:,.2f}",
        }).apply(style.highlight_total_row, axis=1)  # Hide the index
        
        # Define the style for table elements
        df_styled = df_styled.set_properties(**{
            'text-align': 'center', 'font-weight': 'bold', 'border': '1px solid black'
        })
        
        # Display the DataFrame using Streamlit
        st.dataframe(df_styled, use_container_width=True, hide_index=True)

    with col2 :
        col1_1, _, col1_2 = st.columns([7,1,7])

        with col1_1 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])
            
            header_data["pie selected region"] = st.selectbox(
                "Pilih Region ",
                data.get_list_region(df),
            )

            pie_data_left = data.get_proporsi_sales_region(
                df,
                header_data,
            )
            piechart_proporsi_left = graph.piechart_proporsi(pie_data_left.sum(), header_data, category="region")

            st.plotly_chart(piechart_proporsi_left, use_container_width=True)
        
        with col1_2 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal ",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir ",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])

            header_data["pie selected region"] = st.selectbox(
                "Pilih Region  ",
                data.get_list_region(df),
            )

            pie_data_right = data.get_proporsi_sales_region(
                df, 
                header_data,
            )
            piechart_proporsi_right = graph.piechart_proporsi(pie_data_right.sum(), header_data, "region")

            st.plotly_chart(piechart_proporsi_right, use_container_width=True)

    st.divider()

    data_rerata = data.get_rata_rata_region(df, header_data)
    linechart_rerata = graph.linechart_rerata(data_rerata, header_data)
    st.plotly_chart(linechart_rerata, use_container_width=True)
    

def body_kota(df, header_data) :
    proportion_data = data.get_proporsi_produk_kota(df, header_data)
    barchart_porporsi = graph.barchart_proporsi(proportion_data, header_data)
    st.plotly_chart(barchart_porporsi, use_container_width=True)

    st.divider()

    col1, col2 = st.columns([3,5])

    with col1 :
        data_realisasi = data.get_total_pencapaian_keseluruhan(df, header_data)
       # Initialize an empty table or with some default values
        df_realisasi ={
            "Material": data_realisasi.keys(),
            "Target": [0.0 for i in range(len(header_data["selected type"]))],
            "Target YTD": [0.0 for i in range(len(header_data["selected type"]))],
            "Real YTD": data_realisasi.values(),
            "%": [0.0 for i in range(len(header_data["selected type"]))],
        }

        df_realisasi = pd.DataFrame(df_realisasi)

        with st.expander("Input Data Target") :
            # Display editable table for "Target" and "Target YTD" input
            input_realisasi = st.data_editor(df_realisasi[["Material", "Target", "Target YTD"]], num_rows="static", use_container_width=True)
        
        df_realisasi["Target"] = input_realisasi["Target"]
        df_realisasi["Target YTD"] = input_realisasi["Target YTD"]
        df_realisasi["%"] = (df_realisasi["Real YTD"] / input_realisasi["Target YTD"]) * 100

        # Apply icons to the percentage column
        df_realisasi["%"] = df_realisasi["%"].apply(lambda x: style.status_icon(x))

        total_row = {
            "Material": "Total",
            "Target": df_realisasi["Target"].sum(),
            "Target YTD": df_realisasi["Target YTD"].sum(),
            "Real YTD": df_realisasi["Real YTD"].sum(),
            "%": style.status_icon(df_realisasi["%"].apply(lambda x: float(x.split()[1][:-1].replace(",", ""))).mean())  # Average of percentage values
        }

        # Create a DataFrame for the total row
        total_row_df = pd.DataFrame([total_row])

        # Concatenate the total row to the original DataFrame
        df_realisasi = pd.concat([df_realisasi, total_row_df], ignore_index=True)

        df_realisasi.reset_index(drop=True, inplace=True)

        # Format numbers as currency and percentages
        df_styled = df_realisasi.style.format({
            "Target": "{:,.2f}",
            "Target YTD": "{:,.0f}",
            "Real YTD": "{:,.2f}",
        }).apply(style.highlight_total_row, axis=1)  # Hide the index
        
        # Define the style for table elements
        df_styled = df_styled.set_properties(**{
            'text-align': 'center', 'font-weight': 'bold', 'border': '1px solid black'
        })
        
        # Display the DataFrame using Streamlit
        st.dataframe(df_styled, use_container_width=True, hide_index=True)

    with col2 :
        col1_1, _, col1_2 = st.columns([7,1,7])

        with col1_1 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])
            
            header_data["pie selected kota"] = st.selectbox(
                "Pilih Kabupaten/Kota ",
                data.get_list_kota(df),
            )

            pie_data_left = data.get_proporsi_sales_kota(
                df,
                header_data,
            )
            piechart_proporsi_left = graph.piechart_proporsi(pie_data_left.sum(), header_data, category="kota")

            st.plotly_chart(piechart_proporsi_left, use_container_width=True)
        
        with col1_2 :
            header_data["pie start date"] = st.date_input(
                "Masukkan tanggal awal ",
                value=header_data["start date"]
            )
            header_data["pie start date"] = to_datetime(header_data["pie start date"])

            header_data["pie end date"] = st.date_input(
                "Masukkan tanggal akhir ",
                value=header_data["end date"]
            )
            header_data["pie end date"] = to_datetime(header_data["pie end date"])

            header_data["pie selected kota"] = st.selectbox(
                "Pilih Kabupaten/Kota  ",
                data.get_list_kota(df),
            )

            pie_data_right = data.get_proporsi_sales_kota(
                df, 
                header_data,
            )
            piechart_proporsi_right = graph.piechart_proporsi(pie_data_right.sum(), header_data, "kota")

            st.plotly_chart(piechart_proporsi_right, use_container_width=True)

    st.divider()

    data_rerata = data.get_rata_rata_kota(df, header_data)
    linechart_rerata = graph.linechart_rerata(data_rerata, header_data)
    st.plotly_chart(linechart_rerata, use_container_width=True)
    