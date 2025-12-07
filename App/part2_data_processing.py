# Lines 121-240
# CONTINUATION FROM TEAM MEMBER 1

# Memproses dan membersihkan data
def olah_data(df):
    """
    Mengkonversi data ke timezone yang sesuai dan format yang benar
    """
    # Flatten multi-level columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Ensure we have the right columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    if df.index.tzinfo is None:
        df.index = df.index.tz_localize('UTC')
    
    df.index = df.index.tz_convert('US/Eastern')
    df.reset_index(inplace=True)
    
    # Rename kolom ke Bahasa Indonesia
    df.rename(columns={
        'Date': 'Tanggal',
        'Datetime': 'Tanggal',
        'Open': 'Pembukaan',
        'High': 'Tertinggi',
        'Low': 'Terendah',
        'Close': 'Penutupan',
        'Volume': 'Volume'
    }, inplace=True)
    
    return df

# Menghitung metrik penting
def hitung_metrik(df, kurs):
    """
    Menghitung statistik dasar dari data saham dalam USD dan IDR
    """
    harga_terakhir_usd = df['Penutupan'].iloc[-1]
    harga_awal_usd = df['Penutupan'].iloc[0]
    perubahan_usd = harga_terakhir_usd - harga_awal_usd
    perubahan_persen = (perubahan_usd / harga_awal_usd) * 100
    harga_tertinggi_usd = df['Tertinggi'].max()
    harga_terendah_usd = df['Terendah'].min()
    total_volume = df['Volume'].sum()
    
    # Konversi ke IDR
    harga_terakhir_idr = harga_terakhir_usd * kurs
    perubahan_idr = perubahan_usd * kurs
    harga_tertinggi_idr = harga_tertinggi_usd * kurs
    harga_terendah_idr = harga_terendah_usd * kurs
    
    return {
        'harga_terakhir_usd': harga_terakhir_usd,
        'harga_terakhir_idr': harga_terakhir_idr,
        'perubahan_usd': perubahan_usd,
        'perubahan_idr': perubahan_idr,
        'perubahan_persen': perubahan_persen,
        'harga_tertinggi_usd': harga_tertinggi_usd,
        'harga_tertinggi_idr': harga_tertinggi_idr,
        'harga_terendah_usd': harga_terendah_usd,
        'harga_terendah_idr': harga_terendah_idr,
        'total_volume': total_volume
    }

# Menambahkan indikator teknikal
def tambah_indikator(df):
    """
    Menambahkan indikator teknikal seperti SMA dan EMA
    """
    # Make sure we're working with a clean copy
    df = df.copy()
    
    # Ensure Penutupan column is a Series, not DataFrame
    harga_penutupan = df['Penutupan'].squeeze()
    
    # Simple Moving Average
    df['SMA_20'] = ta.trend.sma_indicator(harga_penutupan, window=20)
    df['SMA_50'] = ta.trend.sma_indicator(harga_penutupan, window=50)
    
    # Exponential Moving Average
    df['EMA_20'] = ta.trend.ema_indicator(harga_penutupan, window=20)
    df['EMA_50'] = ta.trend.ema_indicator(harga_penutupan, window=50)
    
    # RSI
    df['RSI'] = ta.momentum.rsi(harga_penutupan, window=14)
    
    return df

# TO BE CONTINUED BY TEAM MEMBER 3...
