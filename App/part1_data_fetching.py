# Lines 1-120
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

# Konstanta kurs USD ke IDR (bisa diupdate secara real-time)
KURS_USD_IDR = 15700  # Default rate, akan diupdate secara otomatis

##########################################################################################
## BAGIAN 1: Fungsi-fungsi untuk Mengambil dan Memproses Data Saham ##
##########################################################################################

# Fungsi untuk mendapatkan kurs USD/IDR terkini
@st.cache_data(ttl=300)  # Cache selama 5 menit
def ambil_kurs_usd_idr():
    """
    Mengambil kurs USD/IDR real-time dari Yahoo Finance
    """
    try:
        kurs_data = yf.download('IDR=X', period='1d', interval='1m', progress=False)
        if not kurs_data.empty:
            if isinstance(kurs_data.columns, pd.MultiIndex):
                kurs_data.columns = kurs_data.columns.get_level_values(0)
            return kurs_data['Close'].iloc[-1]
        else:
            return KURS_USD_IDR  # fallback ke default
    except:
        return KURS_USD_IDR  # fallback ke default

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
        data_saham = yf.download(simbol, start=tanggal_awal, end=tanggal_akhir, interval=interval, progress=False)
    else:
        data_saham = yf.download(simbol, period=periode, interval=interval, progress=False)
    
    return data_saham
