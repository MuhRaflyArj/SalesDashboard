import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import view.style as style

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

   # Menghitung total volume per material (sum across all time periods)
    total_per_material = df_pivot.sum(axis=0).sort_values(ascending=False)

    # Mengambil material names dalam urutan dari terbesar ke terkecil
    sorted_materials = total_per_material.index.tolist()

    # Membuat bar untuk setiap kategori dalam stacked bar dengan proporsi %
    traces = []
    for material in sorted_materials:  # Loop melalui materials yang sudah diurutkan
        volumes = df_pivot[material].tolist()
        # Menghitung persentase kontribusi untuk setiap periode waktu
        percentages = (df_pivot[material] / total_volumes * 100).tolist()
        # Membuat label teks dengan persentase
        text_labels = [f'{p:.1f}%' if p > 0 else '' for p in percentages]
        
        # Menentukan posisi teks agar selalu berada di tengah batang (inside)
        text_positions = 'inside'
        # Menentukan warna teks
        text_colors = ['white' for _ in percentages]  # Use a single color for consistency
        
        # Membuat trace dengan teks berada di tengah
        traces.append(go.Bar(
            name=material,
            x=formatted_labels,
            y=volumes,
            text=text_labels,
            textposition=text_positions,  # Posisi teks selalu di tengah
            textfont=dict(color=text_colors, size=16),  # Ukuran font tetap
            marker_color=style.color(material),
            hovertemplate='<b>%{x}</b><br>%{customdata}<br>Volume: %{y}<br>Persentase: %{text}',
            customdata=[material]*len(volumes)
        ))

    # Inisialisasi figure dengan menambahkan stacked barchart dari data yang disimpan
    fig = go.Figure(data=traces)

    # Menentukan judul plot berdasarkan frekuensi agregasi
    if "selected material" in header_data.keys() :
        if header_data["aggregate"] == 'W':
            title = f'Penjualan Mingguan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
        elif header_data["aggregate"] == 'M':
            title = f'Penjualan Bulanan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
        elif header_data["aggregate"] == 'Y':
            title = f'Penjualan Tahunan {header_data["selected material"]} Berdasarkan Nilai {header_data["selected value"]}'
        else:
            title = 'Penjualan Gasoline'
    else :
        title = "Penjualan LPG"

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

def piechart_proporsi(df, header_data, category=""):
    labels = list(df.index)
    values = list(df[header_data["selected value"]])

    start_date = header_data["pie start date"].strftime("%d-%b-%y")
    end_date = header_data["pie end date"].strftime("%d-%b-%y")

    # Inisialisasi dan membuat piechart pada Plotly
    fig = go.Figure()

    # Plot piechart pada figure dengan hollow (donut)
    fig.add_trace(go.Pie(
        labels=labels, 
        values=values, 
        hole=0.7,  # Membuat piechart berongga di tengah
        domain=dict(x=[0.05, 0.95], y=[0, 1]),  # Mengatur domain agar piechart berada di tengah dan lebih besar
        marker=dict(colors=[style.color(label) for label in labels])
    ))

    annotations = []

    if category == "keseluruhan" :
        annot = dict (
            text=f"{start_date} - {end_date}",
            x=0.5,
            y=-0.05,
            font_size=14,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )

        annotations.append(annot)

    elif category == "region" :
        annot_1 = dict (
            text=f"{start_date} - {end_date}",
            x=0.5,
            y=-0.05,
            font_size=14,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )

        annotations.append(annot_1)

        annot_2 = dict(
            text= f"{header_data['selected region']}",
            x = 0.5,
            y = 1.225,
            font_size=16,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )

        annotations.append(annot_2)

    elif category == "kota" :
        annot_1 = dict (
            text=f"{start_date} - {end_date}",
            x=0.5,
            y=-0.05,
            font_size=14,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )

        annotations.append(annot_1)

        annot_2 = dict(
            text= f"{header_data['pie selected kota']}",
            x = 0.5,
            y = 1.225,
            font_size=16,
            showarrow=False,
            xanchor='center',
            yanchor='top'
        )

        annotations.append(annot_2)

    # Menambahkan informasi pada plot
    fig.update_layout(
        title={
            'text': f'Proporsi Sales {header_data["selected material"]}',
            'y': 0.9,  # Posisi y judul
            'x': 0.5,  # Posisi x judul (align tengah)
            'xanchor': 'center',
            'yanchor': 'top'
        },
        annotations=annotations,
        legend=dict(
            x=0.5,  # Posisi x dari legend (align tengah)
            y=0.5,  # Posisi y dari legend (align tengah)
            xanchor='center',  # Anchor legend di tengah secara horizontal
            yanchor='middle',  # Anchor legend di tengah secara vertikal
            bgcolor="rgba(255, 255, 255, 0)",  # Warna background
            bordercolor="Black",  # Warna border
            font=dict(
                size=10,
            ),
        ),
        height=400,  # Menambah tinggi figure untuk memperbesar pie chart
    )

    return fig  # Mengembalikan plot yang dibuat

def linechart_rerata(df, header_data):
    # Pivot dataframe untuk mendapatkan 'Material Name' sebagai kolom
    df_pivot = df.pivot_table(
        index='Calendar Day',
        columns='Material Name',
        values=["Rerata"],
        aggfunc='sum'
    ).fillna(0)

    # Mengambil labels (Calendar Day) dan materials (Material Name)
    labels = df_pivot.index.tolist()
    materials = df_pivot.columns.levels[1].tolist()  # Mendapatkan 'Material Name'

    # Memproses labels sesuai dengan frekuensi agregasi
    formatted_labels = []
    # Untuk data mingguan
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

    # Membuat garis untuk setiap kategori 'Material Name' dengan format legend hanya nama produk
    traces = []
    for material in materials:
        # Membuat garis untuk Rerata Harian
        rerata_harian = df_pivot['Rerata', material].tolist()
        traces.append(go.Scatter(
            name=material,  # Hanya nama produk yang tampil di legend
            x=formatted_labels,
            y=rerata_harian,
            mode='lines+markers+text',  # Menambahkan teks di titik plot
            line=dict(dash='solid', color=style.color(material)),
            hovertemplate='%{y:.2f}',  # Format hover sesuai permintaan
            text=[f'{y:.2f}' for y in rerata_harian],  # Menampilkan nilai pada setiap titik
            textposition='top center',  # Posisi teks pada titik
            customdata=[material]*len(rerata_harian)
        ))

    # Menambahkan garis baru untuk total dari semua produk
    total_rerata = df_pivot.sum(axis=1).tolist()
    traces.append(go.Scatter(
        name='Total',
        x=formatted_labels,
        y=total_rerata,
        mode='lines+markers+text',  # Menambahkan teks di titik plot
        line=dict(color='black', dash='dash'),  # Menggunakan garis putus-putus untuk total
        hovertemplate='Total: %{y:.2f}',  # Hover untuk total
        text=[f'{y:.2f}' for y in total_rerata],  # Menampilkan nilai total pada setiap titik
        textposition='top center',  # Posisi teks pada titik total
        customdata=['Total']*len(total_rerata),
    ))

    # Inisialisasi figure dengan menambahkan line chart dari data yang disimpan
    fig = go.Figure(data=traces)

    # Menambahkan layout untuk tampilan chart
    fig.update_layout(
        title='Line Chart Rerata Penjualan Produk',
        xaxis_title='Periode',
        yaxis_title=header_data["selected value"],
        height=600,
        legend=dict(
            orientation="h",  # Horizontal orientation for the legend
            yanchor="middle",  # Aligns legend at the bottom of the y position
            y=-0.2,  # Slightly above the chart (1 is top of the chart)
            xanchor="center",  # Center horizontally
            x=0.5  # Center the legend
        ),
        hovermode='x unified'
    )

    return fig

def grouped_barchart_target(df, header_data):
    fig = go.Figure()

    # Create bars for Target, Target YTD, and Real YTD
    for col_name in ["Target", "Target YTD", "Real YTD"]:
        fig.add_trace(go.Bar(
            x=df["Material"],
            y=df[col_name],
            name=col_name,
            text=df[col_name],  # Add text above bars
            textposition="auto"  # Text position
        ))

    # Update layout for the figure
    fig.update_layout(
        barmode="group",
        title=f"Sales Performance {header_data['selected material']}",
        xaxis_title="Produk",
        yaxis_title=header_data["selected value"],
        legend=dict(
            orientation="h",  # Horizontal orientation for the legend
            yanchor="bottom",  # Aligns legend at the bottom of the y position
            y=1,  # Slightly above the chart (1 is top of the chart)
            xanchor="center",  # Center horizontally
            x=0.5  # Center the legend
        ),
        height=400  # Set height of the figure
    )

    return fig