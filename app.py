# Dashboard Analisis Saham dengan Streamlit
# Aplikasi untuk menganalisis data saham secara real-time

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

##########################################################################################
## BAGIAN 1: Fungsi-fungsi untuk Mengambil dan Memproses Data Saham ##
##########################################################################################

# Mengambil data saham dari Yahoo Finance
def ambil_data_saham(simbol, periode, interval):
    """
    Fungsi untuk mengunduh data historis saham
    Parameter:
        simbol: kode ticker saham
        periode: rentang waktu data
        interval: interval waktu per data point
    """
    tanggal_akhir = datetime.now()
    
    if periode == '1minggu':
        tanggal_awal = tanggal_akhir - timedelta(days=7)
        data_saham = yf.download(simbol, start=tanggal_awal, end=tanggal_akhir, interval=interval)
    else:
        data_saham = yf.download(simbol, period=periode, interval=interval)
    
    return data_saham

# Memproses dan membersihkan data
def olah_data(df):
    """
    Mengkonversi data ke timezone yang sesuai dan format yang benar
    """
    if df.index.tzinfo is None:
        df.index = df.index.tz_localize('UTC')
    
    df.index = df.index.tz_convert('US/Eastern')
    df.reset_index(inplace=True)
    
    # Rename kolom ke Bahasa Indonesia
    df.rename(columns={
        'Date': 'Tanggal',
        'Open': 'Pembukaan',
        'High': 'Tertinggi',
        'Low': 'Terendah',
        'Close': 'Penutupan',
        'Volume': 'Volume'
    }, inplace=True)
    
    return df

# Menghitung metrik penting
def hitung_metrik(df):
    """
    Menghitung statistik dasar dari data saham
    """
    harga_terakhir = df['Penutupan'].iloc[-1]
    harga_awal = df['Penutupan'].iloc[0]
    perubahan = harga_terakhir - harga_awal
    perubahan_persen = (perubahan / harga_awal) * 100
    harga_tertinggi = df['Tertinggi'].max()
    harga_terendah = df['Terendah'].min()
    total_volume = df['Volume'].sum()
    
    return harga_terakhir, perubahan, perubahan_persen, harga_tertinggi, harga_terendah, total_volume

# Menambahkan indikator teknikal
def tambah_indikator(df):
    """
    Menambahkan indikator teknikal seperti SMA dan EMA
    """
    # Simple Moving Average
    df['SMA_20'] = ta.trend.sma_indicator(df['Penutupan'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(df['Penutupan'], window=50)
    
    # Exponential Moving Average
    df['EMA_20'] = ta.trend.ema_indicator(df['Penutupan'], window=20)
    df['EMA_50'] = ta.trend.ema_indicator(df['Penutupan'], window=50)
    
    # RSI
    df['RSI'] = ta.momentum.rsi(df['Penutupan'], window=14)
    
    return df

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
        # Ambil dan proses data
        data = ambil_data_saham(kode_saham, periode_waktu, pemetaan_interval[periode_waktu])
        
        if data.empty:
            st.error('❌ Data tidak ditemukan. Pastikan kode saham benar.')
        else:
            data = olah_data(data)
            data = tambah_indikator(data)
            
            # Hitung metrik
            harga_terakhir, perubahan, perubahan_persen, tinggi, rendah, volume = hitung_metrik(data)
            
            # Tampilkan metrik utama
            st.subheader(f'📈 {kode_saham.upper()}')
            
            col_metrik1, col_metrik2, col_metrik3, col_metrik4 = st.columns(4)
            
            with col_metrik1:
                st.metric(
                    label="Harga Terakhir", 
                    value=f"${harga_terakhir:.2f}",
                    delta=f"${perubahan:.2f} ({perubahan_persen:.2f}%)"
                )
            
            with col_metrik2:
                st.metric("Tertinggi", f"${tinggi:.2f}")
            
            with col_metrik3:
                st.metric("Terendah", f"${rendah:.2f}")
            
            with col_metrik4:
                st.metric("Volume", f"{volume:,.0f}")
            
            st.markdown('---')
            
            # Buat grafik harga saham
            st.subheader(f'Grafik Harga {kode_saham.upper()}')
            
            grafik = go.Figure()
            
            # Pilih tipe grafik
            if tipe_grafik == 'Candlestick':
                grafik.add_trace(go.Candlestick(
                    x=data['Tanggal'],
                    open=data['Pembukaan'],
                    high=data['Tertinggi'],
                    low=data['Terendah'],
                    close=data['Penutupan'],
                    name='Harga'
                ))
            elif tipe_grafik == 'Garis':
                grafik.add_trace(go.Scatter(
                    x=data['Tanggal'], 
                    y=data['Penutupan'],
                    mode='lines',
                    name='Harga Penutupan',
                    line=dict(color='#1f77b4', width=2)
                ))
            else:  # Area
                grafik.add_trace(go.Scatter(
                    x=data['Tanggal'], 
                    y=data['Penutupan'],
                    fill='tozeroy',
                    name='Harga Penutupan',
                    line=dict(color='#1f77b4')
                ))
            
            # Tambahkan indikator teknikal yang dipilih
            warna_indikator = {
                'SMA 20': '#ff7f0e',
                'SMA 50': '#2ca02c',
                'EMA 20': '#d62728',
                'EMA 50': '#9467bd'
            }
            
            for indikator in indikator_teknikal:
                if indikator == 'SMA 20':
                    grafik.add_trace(go.Scatter(
                        x=data['Tanggal'], 
                        y=data['SMA_20'], 
                        name='SMA 20',
                        line=dict(color=warna_indikator['SMA 20'], dash='dash')
                    ))
                elif indikator == 'SMA 50':
                    grafik.add_trace(go.Scatter(
                        x=data['Tanggal'], 
                        y=data['SMA_50'], 
                        name='SMA 50',
                        line=dict(color=warna_indikator['SMA 50'], dash='dash')
                    ))
                elif indikator == 'EMA 20':
                    grafik.add_trace(go.Scatter(
                        x=data['Tanggal'], 
                        y=data['EMA_20'], 
                        name='EMA 20',
                        line=dict(color=warna_indikator['EMA 20'], dash='dot')
                    ))
                elif indikator == 'EMA 50':
                    grafik.add_trace(go.Scatter(
                        x=data['Tanggal'], 
                        y=data['EMA_50'], 
                        name='EMA 50',
                        line=dict(color=warna_indikator['EMA 50'], dash='dot')
                    ))
            
            # Format grafik
            grafik.update_layout(
                xaxis_title='Waktu',
                yaxis_title='Harga (USD)',
                height=600,
                hovermode='x unified',
                template='plotly_white'
            )
            
            st.plotly_chart(grafik, use_container_width=True)
            
            # Grafik RSI jika dipilih
            if 'RSI' in indikator_teknikal:
                st.subheader('RSI (Relative Strength Index)')
                grafik_rsi = go.Figure()
                grafik_rsi.add_trace(go.Scatter(
                    x=data['Tanggal'], 
                    y=data['RSI'],
                    name='RSI',
                    line=dict(color='purple')
                ))
                grafik_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
                grafik_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
                grafik_rsi.update_layout(
                    xaxis_title='Waktu',
                    yaxis_title='RSI',
                    height=300,
                    template='plotly_white'
                )
                st.plotly_chart(grafik_rsi, use_container_width=True)
            
            st.markdown('---')
            
            # Tampilkan data dalam tabel
            tab1, tab2 = st.tabs(['📋 Data Historis', '📊 Indikator Teknikal'])
            
            with tab1:
                st.dataframe(
                    data[['Tanggal', 'Pembukaan', 'Tertinggi', 'Terendah', 'Penutupan', 'Volume']].tail(50),
                    use_container_width=True
                )
            
            with tab2:
                kolom_indikator = ['Tanggal', 'SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'RSI']
                kolom_tersedia = [k for k in kolom_indikator if k in data.columns]
                st.dataframe(
                    data[kolom_tersedia].tail(50),
                    use_container_width=True
                )

else:
    # Tampilan awal sebelum data dimuat
    st.info('👈 Pilih parameter di panel samping dan klik "Perbarui Data" untuk memulai analisis')
    
    st.markdown("""
    ### 📌 Fitur Dashboard:
    - **Grafik Interaktif**: Candlestick, Garis, dan Area
    - **Indikator Teknikal**: SMA, EMA, RSI
    - **Data Real-Time**: Update data saham terkini
    - **Analisis Multi-Periode**: Dari 1 hari hingga data maksimal
    
    ### 📖 Cara Menggunakan:
    1. Masukkan kode saham (ticker) di panel samping
    2. Pilih periode waktu dan tipe grafik
    3. Pilih indikator teknikal yang diinginkan
    4. Klik tombol "Perbarui Data"
    """)

# 2C: PANEL SAMPING - HARGA REAL-TIME ############

st.sidebar.markdown('---')
st.sidebar.subheader('💹 Harga Saham Real-Time')

daftar_saham = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

for simbol in daftar_saham:
    try:
        data_realtime = ambil_data_saham(simbol, '1d', '5m')
        if not data_realtime.empty:
            data_realtime = olah_data(data_realtime)
            harga_sekarang = data_realtime['Penutupan'].iloc[-1]
            harga_buka = data_realtime['Pembukaan'].iloc[0]
            selisih = harga_sekarang - harga_buka
            persen_selisih = (selisih / harga_buka) * 100
            
            st.sidebar.metric(
                f"{simbol}", 
                f"${harga_sekarang:.2f}",
                f"{selisih:.2f} ({persen_selisih:.2f}%)"
            )
    except:
        st.sidebar.text(f"{simbol}: Data tidak tersedia")

# Informasi tambahan
st.sidebar.markdown('---')
st.sidebar.subheader('ℹ️ Tentang')
st.sidebar.info(
    'Dashboard ini menyediakan analisis saham real-time dengan berbagai indikator teknikal. '
    'Gunakan panel samping untuk menyesuaikan tampilan sesuai kebutuhan Anda.'
)

st.sidebar.markdown('---')
st.sidebar.caption('💡 Tips: Gunakan indikator teknikal untuk analisis yang lebih mendalam')    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    return data

###############################################
## PART 2: Creating the Dashboard App layout ##
###############################################


# Set up Streamlit page layout
st.set_page_config(layout="wide")
st.title('Real Time Stock Dashboard')


# 2A: SIDEBAR PARAMETERS ############

# Sidebar for user input parameters
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'ADBE')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

# Mapping of time periods to data intervals
interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}


# 2B: MAIN CONTENT AREA ############

# Update the dashboard based on user input
if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    data = process_data(data)
    data = add_technical_indicators(data)
    
    last_close, change, pct_change, high, low, volume = calculate_metrics(data)
    
    # Display main metrics
    st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} USD")
    col2.metric("Low", f"{low:.2f} USD")
    col3.metric("Volume", f"{volume:,}")
    
    # Plot the stock price chart
    fig = go.Figure()
    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=data['Datetime'],
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close']))
    else:
        fig = px.line(data, x='Datetime', y='Close')
    
    # Add selected technical indicators to the chart
    for indicator in indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))
    
    # Format graph
    fig.update_layout(title=f'{ticker} {time_period.upper()} Chart',
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display historical data and technical indicators
    st.subheader('Historical Data')
    st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])
    
    st.subheader('Technical Indicators')
    st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])


# 2C: SIDEBAR PRICES ############

# Sidebar section for real-time stock prices of selected symbols
st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        change = last_price - real_time_data['Open'].iloc[0]
        pct_change = (change / real_time_data['Open'].iloc[0]) * 100
        st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f}%)")

# Sidebar information section
st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various time periods. Use the sidebar to customize your view.')

