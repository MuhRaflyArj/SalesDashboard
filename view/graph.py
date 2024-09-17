import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def barchart_proporsi(df, header_data):
    # Pivot dataframe untuk mendapatkan 'Material Name' sebagai kolom
    df_pivot = df.pivot_table(
        index='Calendar Day',
        columns='Material Name',
        values=header_data["selected value"],
        aggfunc='sum'
    ).fillna(0)

    # Mengambil labels (Calendar Day) dan materials (Material Name)
    labels = df_pivot.index.tolist()
    materials = df_pivot.columns.tolist()

    # Memproses labels sesuai dengan frekuensi agregasi
    formatted_labels = []
    if header_data["aggregate"] == 'W':
        # Untuk data mingguan
        for date in labels:
            day = date.strftime('%d')
            month_year = date.strftime('%b-%Y')
            formatted_label = f"{day} {month_year}"
            formatted_labels.append(formatted_label)
    elif header_data["aggregate"] == 'M':
        # Untuk data bulanan
        for date in labels:
            formatted_label = date.strftime('%b-%Y')
            formatted_labels.append(formatted_label)
    elif header_data["aggregate"] == 'Y':
        # Untuk data tahunan
        for date in labels:
            formatted_label = date.strftime('%Y')
            formatted_labels.append(formatted_label)
    else:
        # Format default jika frekuensi tidak dikenali
        formatted_labels = labels

    # Menghitung total volume per periode waktu
    total_volumes = df_pivot.sum(axis=1)
    max_total_volume = total_volumes.max()  # Mendapatkan nilai maksimum total volume

    # Membuat bar untuk setiap kategori dalam stacked bar dengan proporsi %
    traces = []
    for material in materials:
        volumes = df_pivot[material].tolist()
        # Menghitung persentase kontribusi untuk setiap periode waktu
        percentages = (df_pivot[material] / total_volumes * 100).tolist()
        # Membuat label teks dengan persentase
        text_labels = [f'{p:.1f}%' if p > 0 else '' for p in percentages]
        # Menentukan posisi teks berdasarkan persentase
        text_positions = ['outside' if p > 25 else 'outside' for p in percentages]
        # Menentukan warna teks agar kontras dengan warna batang
        text_colors = ['white' if p > 25 else 'black' for p in percentages]
        traces.append(go.Bar(
            name=material,
            x=formatted_labels,
            y=volumes,
            text=text_labels,
            textposition=text_positions,
            textfont=dict(color=text_colors, size=16),
            hovertemplate='<b>%{x}</b><br>%{customdata}<br>Volume: %{y}<br>Persentase: %{text}',
            customdata=[material]*len(volumes)
        ))

    # Inisialisasi figure dengan menambahkan stacked barchart dari data yang disimpan
    fig = go.Figure(data=traces)

    # Menentukan judul plot berdasarkan frekuensi agregasi
    if header_data["aggregate"] == 'W':
        title = f'Penjualan Mingguan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
    elif header_data["aggregate"] == 'M':
        title = f'Penjualan Bulanan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
    elif header_data["aggregate"] == 'Y':
        title = f'Penjualan Tahunan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
    else:
        title = 'Penjualan Gasoline'

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=title,  # Judul plot
        barmode='stack',  # Membuat barchart menjadi stacked barchart
        xaxis_title='Tanggal',  # Label x-axis
        yaxis_title='Volume',  # Label y-axis
        legend_title='Jenis Bensin',  # Judul legend
        xaxis=dict(
            tickmode='linear',
            tickfont=dict(size=10),  # Menyesuaikan ukuran font agar label tidak tumpang tindih
        ),
        yaxis=dict(
            title='Volume',
            range=[0, 1.25 * max_total_volume]  # Menetapkan limit sumbu y hingga 125% dari nilai maksimum
        ),
        # Tinggi dari grafik
        height=600,
        # Posisi dan warna legend
        legend=dict(
            x=0.9,  # Posisi x dari legend
            y=0.0,  # Posisi y dari legend
            bgcolor="rgba(255, 255, 255, 0.9)",  # Warna background
            bordercolor="Black",  # Warna border
        ),
        margin=dict(b=100),  # Menambahkan margin bawah untuk mencegah label x-axis terpotong
    )

    return fig  # Mengembalikan plot yang dibuat

def piechart_proporsi(df, header_data):
    labels = list(df.index)
    values = list(df[header_data["selected value"]])

    start_date = header_data["pie start"].strftime("%d-%b-%y")
    end_date = header_data["pie end"].strftime("%d-%b-%y")

    # Inisialisasi dan membuat piechart pada Plotly
    fig = go.Figure()

    # Plot piechart pada figure dengan hollow (donut)
    fig.add_trace(go.Pie(
        labels=labels, 
        values=values, 
        hole=0.6,  # Membuat piechart berongga di tengah
        domain=dict(x=[0.1, 0.9], y=[0.5, 1])  # Mengatur domain agar piechart berada di tengah dan lebih besar
    ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title={
            'text': f'Proporsi Sales {header_data["selected material"]}',
            'y': 0.975,  # Posisi y judul
            'x': 0.5,  # Posisi x judul (align tengah)
            'xanchor': 'center',
            'yanchor': 'top'
        },
        annotations=[dict(
            text=f"{start_date} - {end_date}",
            x=0.5,
            y=0.5,
            font_size=14,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )],
        legend=dict(
            x=0.5,  # Posisi x dari legend (align tengah)
            y=0.75,  # Posisi y dari legend (align tengah)
            xanchor='center',  # Anchor legend di tengah secara horizontal
            yanchor='middle',  # Anchor legend di tengah secara vertikal
            bgcolor="rgba(255, 255, 255, 1)",  # Warna background
            bordercolor="Black",  # Warna border
        ),
        height=800,  # Menambah tinggi figure untuk memperbesar pie chart
        width=800,   # Menambah lebar figure untuk memperbesar pie chart
    )

    return fig  # Mengembalikan plot yang dibuat





# ==================================================== #

# Linechart untuk menampilkan tren penjualan pada suatu SPBU
def sales_chart_spbu(df, products, value):
    # Inisialisasi figure Plotly
    fig = go.Figure()

    # Loop untuk semua produk yang dipilih untuk diplot
    for product in products:
        # Ambil data produk tertentu untuk diplot
        data = df.loc[df["Material Name"] == product]
        # Plot setiap titik data yang didapatkan dari DataFrame
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"], # Waktu sebagai x-axis
            y=data[value], # Nilai value yang dipilih sebagai nilai y
            mode="lines+markers",  # Display titik dan garis
            name=product, # Nama suatu garis untuk ditampilkan pada legend
            # Data yang ditampilkan saat mouse hover pada suatu titik
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + value + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=f"Tren {value} per Produk", # Judul dari plot
        xaxis_title="Tanggal", # Label dari x-axis
        yaxis_title=value, # Label dari y-axis
        legend_title="Nama Produk", # Label legend
        template="plotly",
        # Memastikan range y dimulai dari 0 sampai 125% nilai maksimal
        yaxis=dict(range=[0, df[value].max() * 1.25])
    )

    return fig  # Mengembalikan plot yang sudah dibuat

# Linechart untuk menampilkan tren penjualan pada suatu SH
def sales_chart_sh(df, products, value):
    # Inisialisasi figure Plotly
    fig = go.Figure()

    # Loop untuk semua produk yang dipilih untuk diplot
    for product in products:
        # Ambil data produk tertentu untuk diplot
        data = df.loc[df["Material Name"] == product]
        # Plot setiap titik data yang didapatkan dari DataFrame
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"], # Waktu sebagai x-axis
            y=data[value], # Nilai value yang dipilih sebagai nilai y
            mode="lines+markers",  # Display titik dan garis
            name=product, # Nama suatu garis untuk ditampilkan pada legend
            # Data yang ditampilkan saat mouse hover pada suatu titik
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + value + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=f"Tren {value} per Produk", # Judul dari plot
        xaxis_title="Tanggal", # Label dari x-axis
        yaxis_title=value, # Label dari y-axis
        legend_title="Nama Produk", # Label legend
        template="plotly",
        # Memastikan range y dimulai dari 0 sampai 125% nilai maksimal
        yaxis=dict(range=[0, df[value].max() * 1.25])
    )

    return fig  # Mengembalikan plot yang sudah dibuat

# Linechart untuk menampilkan tren penjualan per region
def sales_chart_region(df, regions, value) :
    # Inisialisasi figure Plotly
    fig = go.Figure()

    # Loop untuk semua region yang dipilih untuk diplot
    for region in regions:
        # Ambil data region tertentu untuk diplot
        data = df.loc[df["Sales District"] == region]
        # Plot setiap titik data yang didapatkan dari DataFrame
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"], # Waktu sebagai x-axis
            y=data[value], # Nilai value yang dipilih sebagai nilai y
            mode="lines+markers", # Display titik dan garis
            name=region, # Nama suatu garis untuk ditampilkan pada legend
            # Data yang ditampilkan saat mouse hover pada suatu titik
            hovertemplate="<b>Region:</b>" + region + "<br><b>Date:</b> %{x}<br><b>" + value + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=f"Tren {value} per Wilayah", # Judul dari plot
        xaxis_title="Tanggal", # Label dari x-axis
        yaxis_title=value, # Label dari y-axis
        legend_title="Kabupaten/Kota", # Label legend
        template="plotly",
        # Memastikan range y dimulai dari 0 sampai 125% nilai maksimal
        yaxis=dict(range=[0, df[value].max() * 1.25])
    )

    return fig # Mengembalikan plot yang sudah dibuat

# Linechart untuk menampilkan tren penjualan keseluruhan
def sales_chart_keseluruhan(df, products, value):
    # Inisialisasi figure Plotly
    fig = go.Figure()

    # Loop untuk semua produk yang dipilih untuk diplot
    for product in products:
        # Ambil data produk tertentu untuk diplot
        data = df.loc[df["Material Name"] == product]
        # Plot setiap titik data yang didapatkan dari DataFrame
        fig.add_trace(go.Scatter(
            x=data["Calendar Day"], # Waktu sebagai x-axis
            y=data[value], # Nilai value yang dipilih sebagai nilai y
            mode="lines+markers",  # Display titik dan garis
            name=product, # Nama suatu garis untuk ditampilkan pada legend
            # Data yang ditampilkan saat mouse hover pada suatu titik
            hovertemplate="<b>Product:</b> " + product + "<br><b>Date:</b> %{x}<br><b>" + value + ":</b> %{y:.2f}<extra></extra>"
        ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=f"Tren {value} pada Keseluruhan Data", # Judul dair plot
        xaxis_title="Tanggal", # Label dari x-axis
        yaxis_title=value, # Label dari y-axis
        legend_title="Produk", # Label legend
        template="plotly",
        # Memastikaan range y dimulai dari 0 sampai 125% nilai maksimal
        yaxis=dict(range=[0, df[value].max() * 1.25])
    )

    return fig  # Return the Plotly figure object

# Piechart untuk membandingkan rasio nilai penjualan
def sales_piechart(sales_data, value) :
    # Mengambil nama label dari keys dictionary yang diberikan
    labels = list(sales_data.keys())
    # Mengambil nilai yang akan dibandingkan
    values = [abs(i) for i in sales_data.values()]

    # Inisialisasi dan membuat piechart pada Plotly
    fig = go.Figure()

    # Plot piechart pada figure
    fig.add_trace(go.Pie(
        labels=labels, 
        values=values
    ))

    # Menambahkan informasi pada plot
    fig.update_layout(
        title_text=f"Rasio {value}", # Menambahkan judul
    )

    return fig # Mengembalikan plot yang dibuat

# Barchart untuk membandingkan penjualan satu dengan lainnya
def sales_barchart(data, value, title):
    # Mengambil nama label dari keys dictionary yang diberikan
    labels = list(data.keys())
    # Mengambil nilai yang akan dibandingkan
    values = list(data.values())
    # Mengubah format nilai menjadi x,xxx,xxx untuk ditampilkan
    formatted_values = [f"{value:,.0f}" for value in values]

    # Inisialisasi figure plotly
    fig = go.Figure()

    # Plot barchart pada figure
    fig = go.Figure(data=[go.Bar(
        x=labels, # Label dari beberapa jenis data sebagai x-axis
        y=values, # Nilai yang ditinjau sebagai y-axis
        text=formatted_values, # Menampilkan nilai sebenarnya pada barchart
        textposition="inside" # Menampikan nilai didalam barchart
    )])

    # Menambahkan informasi pada plot
    fig.update_layout(
        title=title, # Judul plot (diberikan dari parameter)
        yaxis_title=value, # Label y-axis sesuai dengan value yang ditinjau
        template="plotly"
    )

    return fig # Mengembalikan plot yang dibuat

# Grouped barchart untuk membandingkan beberapa penjualan
def sales_stacked_barchart(data, value, title) :
    # Mengambil nama label dari keys dictionary yang diberikan
    labels = list(data.keys())
    # Mengambil nilai dari value data yang diberikan
    values = list({key for label in data.values() for key in label})

    # Buat bar untuk setiap kategori dalam grouped bar
    traces = []
    for value in values:
        # Ambil data untuk barchart dari values
        trace_values = [data[label].get(value, 0) for label in labels]
        # Masukkan barchart kedalam list
        traces.append(go.Bar(name=value, x=labels, y=trace_values))

    # Inisialisasi figure dengan menambahkan grouped barchart dari data yang disimpan
    fig = go.Figure(data=traces)

    # # Menambahkan informasi pada plot
    fig.update_layout(
        title=title, # Judul plot (diberikan dari parameter)
        barmode="group", # Membuat barchart menjadi grouped barchart
        xaxis_title="Region", # Label x-axis
        yaxis_title=value, # Label y-axis
        # Posisi dan warna legend
        legend=dict(
            x=0.9, # Posisi x dari legend
            y=0.95, # Posisi y dari legend
            bgcolor="rgba(225, 225, 225, 0.5)", # Warna background
            bordercolor="Black", # Warna broder
        ),
    )

    return fig # Mengembalikan plot yang dibuat