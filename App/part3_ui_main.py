# Lines 241-360
# CONTINUATION FROM TEAM MEMBER 2

###############################################
## BAGIAN 2: Membuat Tampilan Dashboard ##
###############################################

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Saham Indonesia",
    page_icon="📊",
    layout="wide"
)

# Judul utama
st.title('📊 Dashboard Analisis Saham Real-Time')
st.markdown('---')

# 2A: PANEL SAMPING - PENGATURAN ############

st.sidebar.title('⚙️ Pengaturan')
st.sidebar.markdown('---')

# Input parameter dari pengguna
st.sidebar.subheader('Parameter Grafik')
kode_saham = st.sidebar.text_input('Kode Saham', 'AAPL', help='Masukkan ticker saham (contoh: AAPL, GOOGL)')

periode_waktu = st.sidebar.selectbox(
    'Periode Waktu', 
    ['1d', '1minggu', '1mo', '3mo', '1y', 'max'],
    format_func=lambda x: {
        '1d': '1 Hari',
        '1minggu': '1 Minggu', 
        '1mo': '1 Bulan',
        '3mo': '3 Bulan',
        '1y': '1 Tahun',
        'max': 'Maksimal'
    }[x]
)

tipe_grafik = st.sidebar.selectbox(
    'Tipe Grafik', 
    ['Candlestick', 'Garis', 'Area'],
    help='Pilih jenis visualisasi grafik'
)

indikator_teknikal = st.sidebar.multiselect(
    'Indikator Teknikal', 
    ['SMA 20', 'SMA 50', 'EMA 20', 'EMA 50', 'RSI'],
    help='Pilih indikator yang ingin ditampilkan'
)

# Mapping periode ke interval
pemetaan_interval = {
    '1d': '5m',
    '1minggu': '30m',
    '1mo': '1d',
    '3mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}

st.sidebar.markdown('---')

# 2B: AREA KONTEN UTAMA ############

# Tombol untuk memperbarui data
if st.sidebar.button('🔄 Perbarui Data', type='primary', use_container_width=True):
    
    with st.spinner(f'Mengambil data untuk {kode_saham}...'):
        # Ambil kurs USD/IDR
        kurs_idr = ambil_kurs_usd_idr()
        
        # Ambil dan proses data
        data = ambil_data_saham(kode_saham, periode_waktu, pemetaan_interval[periode_waktu])
        
        if data.empty:
            st.error('❌ Data tidak ditemukan. Pastikan kode saham benar.')
        else:
            data = olah_data(data)
            data = tambah_indikator(data)
            
            # Hitung metrik
            metrik = hitung_metrik(data, kurs_idr)
            
            # Tampilkan kurs
            st.info(f'💱 Kurs: 1 USD = Rp {kurs_idr:,.2f}')
            
            # Tampilkan metrik utama
            st.subheader(f'📈 {kode_saham.upper()}')
            
            # Buat dua baris metrik: USD dan IDR
            st.markdown("**💵 Harga dalam USD:**")
            col_usd1, col_usd2, col_usd3, col_usd4 = st.columns(4)
            
            with col_usd1:
                # Format delta text manually with color indicator
                delta_text = f"{metrik['perubahan_usd']:.2f} ({metrik['perubahan_persen']:.2f}%)"
                st.metric(
                    label="Harga Terakhir", 
                    value=f"${metrik['harga_terakhir_usd']:.2f}",
                    delta=delta_text,
                    delta_color="normal"
                )
            
            with col_usd2:
                st.metric("Tertinggi", f"${metrik['harga_tertinggi_usd']:.2f}")
            
            with col_usd3:
                st.metric("Terendah", f"${metrik['harga_terendah_usd']:.2f}")
            
            with col_usd4:
                st.metric("Volume", f"{metrik['total_volume']:,.0f}")
            
            st.markdown("**🇮🇩 Harga dalam IDR:**")
            col_idr1, col_idr2, col_idr3, col_idr4 = st.columns(4)
            
            with col_idr1:
                # Format delta text manually with color indicator
                delta_text_idr = f"{metrik['perubahan_idr']:.0f} ({metrik['perubahan_persen']:.2f}%)"
                st.metric(
                    label="Harga Terakhir", 
                    value=f"Rp {metrik['harga_terakhir_idr']:,.0f}",
                    delta=delta_text_idr,
                    delta_color="normal"
                )
            
            with col_idr2:
                st.metric("Tertinggi", f"Rp {metrik['harga_tertinggi_idr']:,.0f}")
            
            with col_idr3:
                st.metric("Terendah", f"Rp {metrik['harga_terendah_idr']:,.0f}")
            
            with col_idr4:
                st.metric("Volume", f"{metrik['total_volume']:,.0f}")
            
            st.markdown('---')
            
            # TO BE CONTINUED BY TEAM MEMBER 4...
