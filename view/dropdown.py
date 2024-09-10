import streamlit as st

def upload_popup() :
    tab1, tab2 = st.tabs(["Upload Data", "Petunjuk"])

    with tab1 :
        st.write("### Upload Excel Sales")

        data_type = st.radio("Pilih Jenis Data", ("Data LPG", "Data Fuel"))
            
        # Create the file uploader inside the popup
        uploaded_file = st.file_uploader("Pastikan nama sheet adalah `target`", type="xlsx")
    
    with tab2:
        st.markdown("""
        ### Penamaan Sheet
        Pastikan nama sheet dalam excel yang diupload memiliki nama `target` seperti gambar dibawah
        """)

        st.image("./asset/image.png")

        st.markdown("""
        ### Penamaan Kolom
        Pastikan urutan dan nama kolom sesuai seperti urutan berikut

        **Penamaan kolom *Fuel Sales***
        - Calendar Year/Month
        - Calendar Day
        - Region
        - Sales District
        - Sold-to party
        - Ship-To Party
        - SH Name
        - No Lambung
        - Street Name
        - Customer Group
        - Customer Price Group
        - Plant
        - Plant Name
        - Price List Type
        - Material (Merujuk pada kolom kode material)
        - Material (Merujuk pada kolom nama material)
        - Billing Quantity (KL)
        - Volume
        - Harga Faktur
        - \- Hasil Penjualan \-
        - \- Margin \-
        - \- PBBKB \-
        - Net Value

        **Penamaan Kolom *LPG Sales***
        - Calendar Year/Month
        - Calenar Day
        - Region
        - Sales District
        - Sold-to party
        - Ship-To Party
        - SH Name
        - Name 2
        - Street Name
        - Customer group
        - Customer Price Group
        - Plant
        - Plant Name
        - Price List Type
        - Material (Merujuk pada kolom kode material)
        - Material (Merujuk pada kolom nama material)
        - Billing Quantity (MT)
        - Harga Faktur
        - \- Hasil Penjualan \-
        - \- Margin \-
        - \- PBBKB \-
        - Net Value
        """)

    return data_type, uploaded_file