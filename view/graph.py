import plotly.graph_objects as go
import plotly.express as px

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