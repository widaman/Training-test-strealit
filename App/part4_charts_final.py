# Lines 361-475
# CONTINUATION FROM TEAM MEMBER 3

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
    - **Dual Currency**: Tampilan harga dalam USD dan IDR
    
    ### 📖 Cara Menggunakan:
    1. Masukkan kode saham (ticker) di panel samping
    2. Pilih periode waktu dan tipe grafik
    3. Pilih indikator teknikal yang diinginkan
    4. Klik tombol "Perbarui Data"
    """)

# 2C: PANEL SAMPING - HARGA REAL-TIME ############

st.sidebar.markdown('---')
st.sidebar.subheader('💹 Harga Saham Real-Time')

# Ambil kurs untuk sidebar
kurs_sidebar = ambil_kurs_usd_idr()

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
            
            # Konversi ke IDR
            harga_sekarang_idr = harga_sekarang * kurs_sidebar
            
            # Format delta without dollar sign so Streamlit can detect sign
            delta_text = f"{selisih:.2f} ({persen_selisih:.2f}%)"
            
            st.sidebar.metric(
                f"{simbol}", 
                f"${harga_sekarang:.2f} / Rp {harga_sekarang_idr:,.0f}",
                delta_text,
                delta_color="normal"
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
st.sidebar.caption('💡 Tips: Gunakan indikator teknikal untuk analisis yang lebih mendalam')
