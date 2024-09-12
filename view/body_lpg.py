import streamlit as st
import view.header_lpg as header
import model.data as data
import view.graph as graph

# Body jenis visualisasi data per-SH
def body_sh(df) :
    # Mengambil data yang diperlukan header dari DataFrame
    list_region, dict_sh, dict_product = data.get_header_data_sh(df)
    # Menampilkan header dan mengembalikan data yang dipilih oleh user pada header
    header_data = header.header_sh(list_region, dict_sh, dict_product)
    
    st.divider() # Garis pemisah antara header dan visualisasi

    # Mengambil data tren penjualan berdasarkan sh 
    # dan nilai yang dipilih dengan aggregate tertentu
    sales_data = data.get_sales_data_sh(
        df,
        header_data["selected sh"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
        header_data["aggregate"]
    )

    # Mengambil data perbandingan PSO 
    # (key = jenis produk (PSO/standar), value = total nilai)
    pso_data = data.get_total_pso_sh(
        df,
        header_data["selected sh"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    # Mengambil dictionary total nilai (key = product, value = total)
    total_sales_dict = data.get_total_sales_sh(
        df,
        header_data["selected sh"],
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
    )

    # ========================= #
    # 2 kolom pada baris pertama untuk menampung total nilai dan grafik tren
    col1_1, col1_2 = st.columns([1,4])

    # Isi kolom untuk total nilai
    with col1_1 :
        st.write(" "); st.write(" ") # Tambah 2 baris kosong
        # Judul pada kolom total nilai
        st.write(f"**Total Nilai {header_data['selected value']}**")
        
        st.divider() # Garis pemisah

        # 2 Kolom pada total nilai untuk nama produk dan total nilai
        col1_1_1, col1_1_2 = st.columns([2, 1])

        # Menulis nama produk pada kolom pertama
        with col1_1_1 :
            st.write("**Produk**") # Nama kolom
            for produk in total_sales_dict.keys() :
                st.write(produk)

        # Menulis total nilai dari suatu produk pada kolom kedua
        with col1_1_2 :
            st.write("**Total**") # Nama kolom
            for total in total_sales_dict.values() :
                st.write("{:,.0f}".format(total))

    # Isi kolom untuk grafik tren penjualan suatu produk pada SH tertentu
    with col1_2 :
        # Buat chart tren penjualan antar produk
        fig_sales_linechart = graph.sales_chart_sh(
            sales_data, 
            header_data["selected product"], 
            header_data["selected value"]
        )
        # Tampilkan chart tren penjualan pada streamlit
        st.plotly_chart(fig_sales_linechart, use_column_width=True)

    # ========================= #
    # 3 Kolom pada baris kedua untuk menampung rasio penjualan produk perbandingan PSO dan standar, 
    # dan perbandingan setiap produk
    col2_1, col2_2, col2_3 = st.columns([3,2,5])

    # Isi kolom untuk rasio penjualan
    with col2_1 :
        # Buat piechart rasio penjualan
        sales_piechart = graph.sales_piechart(total_sales_dict, header_data["selected value"])
        # Tampilkan piechart rasio penjualan pada streamlit
        st.plotly_chart(sales_piechart, use_column_width=True)

    # Isi kolom untuk perbandingan penjualan PSO dan standar
    with col2_2 :
        # Buat barchart untuk perbandingan penjualan PSO dan standar
        pso_barchart = graph.sales_barchart(pso_data, header_data["selected value"], f"Perbandingan {header_data['selected value']} PSO dan Standar")
        # Tampilkan barchart perbandingan PSO pada streamlit
        st.plotly_chart(pso_barchart, use_column_width=True)

    # Isi kolom untuk perbandingan penjualan setiap produk
    with col2_3 :
        # Buat barchart untuk perbandingan penjualan setiap produk
        sales_barchart = graph.sales_barchart(total_sales_dict, header_data["selected value"], f"Perbandingan {header_data['selected value']} Setiap Produk")
        # Tampilkan barchart perbandingan penjualan pada streamlit
        st.plotly_chart(sales_barchart, use_column_width=True)

# Body jenis visualisasi data per-region
def body_region(df) :
    # Mengambil data yang diperlukan header dari DataFrame
    list_region, dict_product = data.get_header_data_region(df)
    # Menampilkan header dan mengembalikan data yang dipilih oleh user pada header
    header_data = header.header_region(list_region, dict_product)

    st.divider() # Garis pemisah antara header dan visualisasi

    # Mengambil data sales berdasarkan region, produk dan nilai yang dipilih
    sales_data = data.get_sum_region(
        df,
        header_data["selected region"],
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    # Mengambil data untuk perbandingan penjualan dari sales_data 
    # (key = region, value = nilai total penjualan)
    pie_data = {
        region : round(sum(value.values())) for region, value in sales_data.items()
    }

    # Mengambil data untuk perbandingan penjualan produk PSO dan Standar dari region yang dipilih
    pso_data = data.get_total_pso_region(
        df,
        header_data["selected region"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    # Mengambil data untuk menampilkan tren penjualan region yang dipilih (filtered DataFrame)
    timed_sales_data = data.get_sales_data_region(
        df,
        header_data["selected region"],
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
        header_data["aggregate"]
    )

    # ========================= #
    # 2 kolom pada baris pertama untuk menampung total nilai
    # dan perbandingan penjualan setiap produk pada beberapa region
    col1_1, col1_2 = st.columns([1,3])

    # Isi kolom untuk total nilai
    with col1_1 :
        st.write(" "); st.write(" ") # Tambah 2 baris kosong
        # Judul pada kolom total nilai
        st.write(f"**Total Nilai {header_data['selected value']}**")
        
        st.divider() # Garis pemisah

        # 2 Kolom pada total nilai untuk nama produk dan total nilai
        col1_1_1, col1_1_2 = st.columns([3,2])
        
        # Menulis judul kolom untuk total nilai
        with col1_1_1 :
            st.write("**Kabupaten/Kota**")
        with col1_1_2 :
            st.write(header_data["selected value"])

        # Menulis nama region dan total penjualan
        for region, value in sales_data.items() :
            with col1_1_1 :
                st.write(region) # Menulis nama setiap region
            with col1_1_2 :
                # Menulis total penjualan dari region tertentu
                st.write("{:,.0f}".format(round(sum(value.values()))))

    # Isi kolom untuk grafik tren penjualan setiap produk pada region tertentu
    with col1_2 :
        # Buat grouped barchart untuk menampilkan penjualan setiap produk pada region tertentu
        fig_sales_barchart = graph.sales_stacked_barchart(
            sales_data, 
            header_data["selected value"], 
            f"Perbandingan {header_data['selected value']} Produk per Wilayah"
        )
        # Menampilkan grouped barchart pada streamlit
        st.plotly_chart(fig_sales_barchart, use_container_width=True)

    # ========================= #
    # 3 kolom pada baris kedua untuk menampung rasio penjualan, 
    # perbandingan penjualan PSO dan standar, dan tren penjualan
    col2_1, col2_2, col2_3 = st.columns([3,2,5])

    # Isi kolom untuk piechart rasio penjualan antar region
    with col2_1 :
        # Buat piechart rasio penjualan antar region
        fig_sales_piechart = graph.sales_piechart(
            pie_data, 
            header_data["selected value"]
        )
        # Tampilkan piechart rasio penjualan pada streamlit
        st.plotly_chart(fig_sales_piechart, use_container_width=True)
    
    # Isi kolom untuk perbandingan penjualan produk PSO dan standar
    with col2_2 :
        # Buat barchart perbandingan penjualan produk PSO dan standar
        fig_pso_barchart = graph.sales_barchart(
            pso_data, 
            header_data["selected value"], 
            f"Perbandingan {header_data['selected value']} PSO dan Standar"
        )
        # Tampilkan barchart perbandingan penjualan pada streamlit
        st.plotly_chart(fig_pso_barchart, use_container_width=True)

    # Isi kolom untuk grafik tren penjualan antar region
    with col2_3 :
        # Buat chart tren penjualan antar region
        fig_sales_linechart = graph.sales_chart_region(
            timed_sales_data,
            header_data["selected region"],
            header_data["selected value"]
        )
        # Tampilkan chart tren penjualan pada streamlit
        st.plotly_chart(fig_sales_linechart, use_container_width=True)

# Body jenis visualisasi data keseluruhan
def body_keseluruhan(df) :
    # Mengambil data yang diperlukan header dari DataFrame
    list_product = data.get_product_keseluruhan(df)
    # Menampilkan header dan mengembalikan data yang dipilih oleh user pada header
    header_data = header.header_keseluruhan(list_product)

    st.divider() # Garis pemisah antara header dan visualisasi

    # Mengambil data tren penjualan keseluruhan berdasarkan produk yang dipilih
    sales_data = data.get_sales_data_keseluruhan(
        df,
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"],
        header_data["aggregate"]
    )

    # Mengambil data penjualan setiap produk (key = nama produk, value = total penjualan)
    sales_numbers = data.get_sum_keseluruhan(
        df,
        header_data["selected product"],
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    # Mengambil data penjualan produk PSO dan standar 
    # (key = jenis produk (PSO atau standar), value = total penjualan)
    total_pso = data.get_total_pso_keseluruhan(
        df,
        header_data["selected value"],
        header_data["start date"],
        header_data["end date"]
    )

    # ========================= #
    # Buat chart tren penjualan antar produk
    fig_sales_linechart = graph.sales_chart_keseluruhan(
        sales_data, 
        header_data["selected product"], 
        header_data["selected value"]
    )
    # Tampilkan chart tren penjualan antar produk pada streamlit
    st.plotly_chart(fig_sales_linechart, use_container_width=True)

    # ========================= #
    # 2 kolom pada baris kedua untuk menampung chart perbandingan penjualan pso dan standar 
    # dan perbandingan penjualan berdasarkan jenis produk
    col2_1, col2_2 = st.columns([1,3])

    # Isi kolom untuk perbandiangan penjualan produk PSO dan standar
    with col2_1 :
        # Buat barchart untuk perbandingan penjualan produk PSO dan standar
        fig_pso_barchart = graph.sales_barchart(
            total_pso, header_data["selected value"], 
            f"Perbandingan {header_data['selected value']} PSO dan Standar"
        )
        # Tampilkan barchart pada streamlit
        st.plotly_chart(fig_pso_barchart, use_container_width=True)

    # Isi kolom untuk perbandingan penjualan antar produk yang dipilih
    with col2_2 :
        # Buat barchart untuk perbandingan penjualan antar produk
        fig_sales_barchart = graph.sales_barchart(sales_numbers, 
            header_data["selected value"], 
            f"Perbandingan {header_data['selected value']} Berdasarkan Jenis Produk"
        )
        # Tampilkan barchart pada streamlit
        st.plotly_chart(fig_sales_barchart, use_container_width=True)

    # ========================= #
    # 2 kolom pada baris ketiga untuk menampung chart perbandingan penjualan antar produk 
    # dan total nilai penjualan
    col3_1, col3_2 = st.columns([3,7])

    # Isi kolom untuk rasio penjualan
    with col3_1 :
        # Buat piechart rasio penjualan
        fig_sales_piechart = graph.sales_piechart(
            sales_numbers, 
            header_data["selected value"]
        )
        # Tampilkan piechart rasio penjualan pada streamlit
        st.plotly_chart(fig_sales_piechart, use_container_width=True)

    # Isi kolom untuk total nilai penjualan setiap produk
    with col3_2 :
        st.write(" "); st.write(" ") # Tambah 2 baris kosong
        # Judul pada kolom total nilai
        st.write(f"**Total Nilai {header_data['selected value']}**")

        st.divider() # Garis pemisah

        # 2 Kolom pada total nilai untuk nama produk dan total nilai
        col3_2_1, col3_2_2 = st.columns([1,2])
        
        # Menulis nama kolom
        with col3_2_1 :
            st.write("**Produk**")  
        with col3_2_2 :
            st.write(f"**{header_data['selected value']}**")

        # Menulis nama produk dan total penjualan
        for product, value in sales_numbers.items() :
            with col3_2_1 :
                st.write(product) # Menulis nama setiap produk
            with col3_2_2 :
                # Menulis total penjualan dari produk tertentu
                st.write("{:,.0f}".format(round(value)))