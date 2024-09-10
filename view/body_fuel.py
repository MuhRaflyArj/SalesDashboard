import streamlit as st
import view.header_fuel as header
import view.graph as graph
import model.data as data

def body_spbu(df) :
    list_region, dict_lambung, dict_product = data.get_header_data_spbu(df)
    header_data = header.header_spbu(list_region, dict_lambung, dict_product)
    
    sales_data = data.get_sales_data_spbu(
        df, 
        header_data["selected lambung"], 
        header_data["selected value"],
        header_data["start date"], 
        header_data["end date"], 
        aggregate=header_data["aggregate"]
    )

    sales_chart = graph.sales_chart_spbu(
        sales_data,
        header_data["selected product"], 
        header_data["selected value"],
    )

    st.divider()

    col1_1, col1_2 = st.columns([1, 3])

    with col1_1 :
        st.write(f"**Total Nilai {header_data['selected value']}**")
        st.divider()
        
        col1_1_1, col1_1_2 = st.columns([2, 1])
        total_sales_dict = data.get_total_sales_spbu(
            df,
            header_data["selected lambung"],
            header_data["selected product"],
            header_data["selected value"],
            header_data["start date"],
            header_data["end date"],
        )
        with col1_1_1 :
            st.write("**Produk**")
            for produk in total_sales_dict.keys() :
                st.write(produk)

        with col1_1_2 :
            st.write("**Total**")
            for total in total_sales_dict.values() :
                st.write("{:,.0f}".format(total))
        

    with col1_2:
        st.plotly_chart(sales_chart, use_container_width=True)

    col2_1, col2_2, col2_3 = st.columns([2,3,4])
    with col2_1 :
        sales_piechart = graph.sales_piechart(total_sales_dict, header_data["selected value"])
        st.plotly_chart(sales_piechart, use_container_width=True)

    with col2_2 :
        total_pso = data.get_total_pso_spbu(
            df,
            header_data["selected lambung"],
            header_data["selected value"],
            header_data["start date"],
            header_data["end date"],
        )

        pso_barchart = graph.sales_barchart(total_pso, header_data["selected value"], f"Perbandingan {header_data['selected value']} PSO dan Standar")
        st.plotly_chart(pso_barchart, use_container_width=True)

    with col2_3 :
        sales_barchart = graph.sales_barchart(total_sales_dict, header_data["selected value"], f"Perbandingan {header_data['selected value']} Setiap Produk")
        st.plotly_chart(sales_barchart, use_container_width=True)

def body_region(df) :
    list_region, dict_product = data.get_header_data_region(df)
    header_data = header.header_region(list_region, dict_product)

    st.divider()

    sales_data = data.get_sum_region(
        df, 
        header_data["selected region"],
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
    )

    col1_1, col1_2 = st.columns([1,3])

    with col1_2 :
        fig_sales_barchart = graph.sales_stacked_barchart(sales_data, header_data["selected value"], f"Perbandingan {header_data['selected value']} Produk per Wilayah")
        st.plotly_chart(fig_sales_barchart, use_container_width=True)

    with col1_1 :
        st.write(f"**Total Nilai {header_data['selected value']}**")
        st.divider()

        col1_1_1, col1_1_2 = st.columns([3,2])
        for region, value in sales_data.items() :
            with col1_1_1 :
                st.write(region)
            with col1_1_2 :
                st.write("{:,.0f}".format(round(sum(value.values()))))

    col2_1, col2_2, col2_3 = st.columns([3,2,5])

    pie_data = {
        region : round(sum(value.values())) for region, value in sales_data.items()
    }

    pso_data = data.get_total_pso_region(
        df, 
        header_data["selected region"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    timed_sales_data = data.get_sales_data_region(
        df,
        header_data["selected region"],
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
        header_data["aggregate"]
    )

    with col2_1 :
        fig_sales_piechart = graph.sales_piechart(pie_data, header_data["selected value"])
        st.plotly_chart(fig_sales_piechart, use_container_width=True)

    with col2_2 :
        fig_pso_barchart = graph.sales_barchart(pso_data, header_data["selected value"], f"Perbandingan {header_data['selected value']} PSO dan Standar")
        st.plotly_chart(fig_pso_barchart, use_container_width=True)

    with col2_3 :
        fig_sales_linechart = graph.sales_chart_region(
            timed_sales_data,
            header_data["selected region"],
            header_data["selected value"]    
        )
        st.plotly_chart(fig_sales_linechart, use_container_width=True)

def body_keseluruhan(df) :
    list_product = data.get_product_keseluruhan(df)
    header_data = header.header_keseluruhan(list_product)

    st.divider()

    sales_data = data.get_sales_data_keseluruhan(
        df, 
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
        header_data["aggregate"]
    )

    fig_sales_linechart = graph.sales_chart_keseluruhan(sales_data, header_data["selected product"], header_data["selected value"])
    st.plotly_chart(fig_sales_linechart, use_container_width=True)

    col1_1, col1_2 = st.columns([1,3])

    with col1_1 :
        sales_numbers = data.get_sum_keseluruhan(
            df, 
            header_data["selected product"], 
            header_data["selected value"],
            header_data["start date"],
            header_data["end date"]
        )

        total_pso = data.get_total_pso_keseluruhan(
            df, 
            header_data["selected value"],
            header_data["start date"],
            header_data["end date"]
        )

        fig_pso_barchart = graph.sales_barchart(total_pso, header_data["selected value"], f"Perbandingan {header_data['selected value']} PSO dan Standard")
        st.plotly_chart(fig_pso_barchart, use_container_width=True)

        
    with col1_2 :
        fig_sales_barchart = graph.sales_barchart(sales_numbers, header_data["selected value"], f"Perbandingan {header_data['selected value']} Berdasarkan Jenis Produk")
        st.plotly_chart(fig_sales_barchart, use_container_width=True)

    col2_1, col2_2 = st.columns([3,7])

    with col2_1 :
        fig_sales_piechart = graph.sales_piechart(sales_numbers, header_data["selected value"])
        st.plotly_chart(fig_sales_piechart, use_container_width=True)

    with col2_2 :

        col2_2_1, col2_2_2 = st.columns([1,2])

        with col2_2_1 :
            st.write("**Produk**")
            
        with col2_2_2 :
            st.write(f"**{header_data['selected value']}**")

        for product, value in sales_numbers.items() :
            with col2_2_1 :
                st.write(product)
            with col2_2_2 :
                st.write("{:,.0f}".format(round(value)))
        
    