import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Kalkulator Perhitungan Kadar Thiamin",
    page_icon="🧪",
    layout="wide"
)

# Inisialisasi State Halaman
if 'started' not in st.session_state:
    st.session_state.started = False

# ==========================================
# HALAMAN DEPAN
# ==========================================
if not st.session_state.started:
    st.markdown("<h1 style='text-align: center;'>Kalkulator Pengukuran Kadar Thiamin dalam Sampel menggunakan Spektrofotometer UV-Vis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Aplikasi bantu analisis laboratorium kuantitatif untuk penyiapan larutan, kurva kalibrasi, perhitungan kadar sampel, dan kontrol presisi.</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Mulai Kalkulator", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()

# ==========================================
# BAGIAN UTAMA KALKULATOR
# ==========================================
else:
    # Sidebar Tombol Kembali
    with st.sidebar:
        st.header("⚙️ Navigasi")
        if st.button("⬅️ Kembali ke Halaman Utama"):
            st.session_state.started = False
            st.rerun()
        st.divider()
        st.info("Gunakan tab di kanan untuk mengakses setiap fitur perhitungan.")

    st.title("🧪 Kalkulator Analisis Thiamin (UV-Vis)")
    
    # Tab Navigasi Fitur
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Larutan Induk",
        "2. Larutan Standar",
        "3. Deret Standar",
        "4. Data Hasil Pengujian",
        "5. Perhitungan Sampel",
        "6. Kontrol Presisi"
    ])

    # ------------------------------------------
    # FITUR 1: Pembuatan Larutan Induk Thiamin
    # ------------------------------------------
    with tab1:
        st.header("Pembuatan Larutan Induk Thiamin")
        st.write("Menghitung bobot thiamin murni yang harus ditimbang.")
        
        col1, col2 = st.columns(2)
        with col1:
            c_induk_target = st.number_input("Konsentrasi Larutan Induk Thiamin (mg/L)", min_value=0.0, value=100.0, step=10.0, key="c_induk_t1")
            v_induk_target = st.number_input("Volume (L)", min_value=0.0, value=1.0, step=0.1, key="v_induk_t1")
        
        # Rumus: konsentrasi larutan induk (mg/L) * volume (L) = gram
        bobot_thiamin_g = (c_induk_target * v_induk_target) 
        
        with col2:
            st.subheader("Hasil Perhitungan:")
            st.number_input("Bobot Standar Thiamin (g)", value=float(bobot_thiamin_g), format="%.2f", disabled=True)
            st.info(f"💡 **Petunjuk:** Timbang **{bobot_thiamin_g:.2f} gram** Thiamin murni kemudian dilarutkan dalam labu takar hingga volume **{v_induk_target} L**.")

    # ------------------------------------------
    # FITUR 2: Pembuatan Larutan Standar Thiamin
    # ------------------------------------------
    with tab2:
        st.header("Pembuatan Larutan Standar Thiamin")
        st.write("Menghitung volume larutan induk yang dipipet untuk membuat larutan standar intermediet.")
        
        col1, col2 = st.columns(2)
        with col1:
            c_induk_f2 = st.number_input("Konsentrasi Larutan Induk (mg/L)", min_value=0.0001, value=100.0, step=10.0, key="c_induk_t2")
            c_standar_target = st.number_input("Konsentrasi Larutan Standar (mg/L)", min_value=0.0, value=10.0, step=1.0, key="c_std_t2")
            v_standar_target = st.number_input("Volume (mL)", min_value=0.0, value=100.0, step=5.0, key="v_std_t2")
        
        # Rumus: (c_std * v_std) / c_induk
        v_induk_dibutuhkan = (c_standar_target * v_standar_target) / c_induk_f2 if c_induk_f2 > 0 else 0.0
        
        with col2:
            st.subheader("Hasil Perhitungan:")
            st.number_input("Volume Larutan Induk (mL)", value=float(v_induk_dibutuhkan), format="%.4f", disabled=True)
            st.info(f"💡 Pipet **{v_induk_dibutuhkan:.4f} mL** larutan induk {c_induk_f2} mg/L ke dalam labu ukur **{v_standar_target} mL**, lalu encerkan dengan pelarut hingga tanda batas.")

    # ------------------------------------------
    # FITUR 3: Pembuatan Deret Standar Thiamin
    # ------------------------------------------
    with tab3:
        st.header("Pembuatan Deret Standar Thiamin")
        
        c_std_pembawa = st.number_input("Konsentrasi Larutan Standar yang Digunakan (mg/L)", min_value=0.0001, value=10.0, step=1.0, key="c_std_t3")
        jumlah_deret = st.number_input("Jumlah Deret Standar", min_value=1, max_value=20, value=5, step=1)
        
        st.write("---")
        st.subheader("Masukkan Parameter Setiap Deret Standar:")
        
        data_deret = []
        for i in range(int(jumlah_deret)):
            st.markdown(f"**Deret Standar Ke-{i+1}**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                c_deret = st.number_input(f"Konsentrasi Deret Standar (mg/L) #{i+1}", min_value=0.0, value=float((i+1)*2), key=f"c_deret_{i}")
            with col_b:
                v_deret = st.number_input(f"Volume Deret Standar (mL) #{i+1}", min_value=0.0, value=50.0, key=f"v_deret_{i}")
            
            # Rumus: (c_deret * v_deret) / c_std
            v_std_dibutuhkan = (c_deret * v_deret) / c_std_pembawa if c_std_pembawa > 0 else 0.0
            
            with col_c:
                st.number_input(f"Volume Larutan Standar (mL) #{i+1}", value=float(v_std_dibutuhkan), format="%.4f", disabled=True, key=f"v_std_out_{i}")
            
            data_deret.append({
                "Deret Ke-": i+1,
                "Konsentrasi Deret Standar (mg/L)": c_deret,
                "Volume Deret Standar (mL)": v_deret,
                "Volume Larutan Standar (mL)": v_std_dibutuhkan
            })
            
        df_deret = pd.DataFrame(data_deret)
        st.session_state['df_deret'] = df_deret
        
        st.subheader("Tabel Ringkasan Pembuatan Deret Standar")
        st.dataframe(df_deret, use_container_width=True)

    # ------------------------------------------
    # FITUR 4: Data Hasil Pengujian (Kurva Kalibrasi)
    # ------------------------------------------
    with tab4:
        st.header("Data Hasil Pengujian (Kurva Kalibrasi)")
        
        if 'df_deret' not in st.session_state or st.session_state['df_deret'].empty:
            st.warning("Silakan isi data pada tab '3. Deret Standar' terlebih dahulu.")
        else:
            df_input_abs = st.session_state['df_deret'][["Deret Ke-", "Konsentrasi Deret Standar (mg/L)"]].copy()
            
            st.write("Masukkan nilai Absorbansi untuk masing-masing konsentrasi deret standar:")
            
            absorbansi_list = []
            for idx, row in df_input_abs.iterrows():
                col_x, col_y = st.columns(2)
                with col_x:
                    st.text(f"Deret {int(row['Deret Ke-'])}: {row['Konsentrasi Deret Standar (mg/L)']} mg/L")
                with col_y:
                    abs_val = st.number_input(f"Absorbansi (Deret {int(row['Deret Ke-'])})", min_value=0.0, value=0.1 * (idx + 1), format="%.4f", key=f"abs_in_{idx}")
                    absorbansi_list.append(abs_val)
            
            df_input_abs['Absorbansi'] = absorbansi_list
            x = df_input_abs['Konsentrasi Deret Standar (mg/L)'].values
            y = df_input_abs['Absorbansi'].values
            
            # Perhitungan Regresi Linier
            if len(x) >= 2:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                r_squared = r_value ** 2
                
                st.session_state['slope'] = slope
                st.session_state['intercept'] = intercept
                
                st.divider()
                st.subheader("📊 Hasil Kurva Kalibrasi")
                
                col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                col_res1.metric("Intercept (a)", f"{intercept:.6f}")
                col_res2.metric("Slope (b)", f"{slope:.6f}")
                col_res3.metric("Koefisien Korelasi (r)", f"{r_value:.6f}")
                col_res4.metric("Koefisien Determinasi (R²)", f"{r_squared:.6f}")
                
                # Plot Kurva
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.scatter(x, y, color='blue', label='Data Standar')
                ax.plot(x, intercept + slope * x, color='red', label=f'y = {slope:.4f}x + {intercept:.4f}')
                ax.set_xlabel('Konsentrasi (mg/L)')
                ax.set_ylabel('Absorbansi')
                ax.set_title('Kurva Kalibrasi Thiamin')
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.6)
                st.pyplot(fig)
            else:
                st.error("Dibutuhkan minimal 2 data deret standar untuk regresi linier.")

    # ------------------------------------------
    # FITUR 5: Perhitungan Konsentrasi Sampel
    # ------------------------------------------
    with tab5:
        st.header("Perhitungan Konsentrasi Sampel")
        
        if 'slope' not in st.session_state or 'intercept' not in st.session_state:
            st.warning("Silakan lengkapi regresi pada tab '4. Data Hasil Pengujian' terlebih dahulu.")
        else:
            slope = st.session_state['slope']
            intercept = st.session_state['intercept']
            
            st.info(f"Persamaan Regresi yang Digunakan: **y = {slope:.6f}x + ({intercept:.6f})**")
            
            rerata_bobot_tablet = st.number_input("Rerata Bobot Tablet (kg)", min_value=0.000001, value=0.0005, format="%.6f", key="bobot_tab")
            n_pengulangan = st.number_input("Pengulangan (Jumlah Sampel)", min_value=1, max_value=20, value=3, step=1)
            
            results_sampel = []
            
            for j in range(int(n_pengulangan)):
                st.markdown(f"**Pengulangan Sampel Ke-{j+1}**")
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    w_sampel = st.number_input(f"Bobot Sampel (gram) #{j+1}", min_value=0.0001, value=0.1, format="%.4f", key=f"w_smp_{j}")
                with c2:
                    v_sampel = st.number_input(f"Volume Sampel (mL) #{j+1}", min_value=0.1, value=100.0, key=f"v_smp_{j}")
                with c3:
                    abs_sampel = st.number_input(f"Absorbansi Sampel #{j+1}", min_value=0.0, value=0.3, format="%.4f", key=f"abs_smp_{j}")
                
                # Perhitungan:
                # 1. Konsentrasi Terukur (mg/L) = (Abs - Intercept) / Slope
                c_terukur = (abs_sampel - intercept) / slope if slope != 0 else 0.0
                
                # 2. Kadar Thiamin pada Sampel (mg/kg) = (Konsentrasi Terukur (mg/L) * Volume Sampel (L)) / Bobot Sampel (kg)
                # Volume (mL) -> L (/1000), Bobot (g) -> kg (/1000). Konversi saling menghilangkan, jadi (C * V_mL) / W_g
                kadar_mg_kg = (c_terukur * v_sampel) / w_sampel if w_sampel > 0 else 0.0
                
                # 3. Kadar Thiamin per Tablet (mg/tablet) = Rerata Bobot Tablet (kg) * Kadar Sampel (mg/kg)
                kadar_per_tablet = rerata_bobot_tablet * kadar_mg_kg
                
                results_sampel.append({
                    "Pengulangan": j + 1,
                    "Bobot Sampel (g)": w_sampel,
                    "Volume Sampel (mL)": v_sampel,
                    "Absorbansi": abs_sampel,
                    "Konsentrasi Terukur (mg/L)": c_terukur,
                    "Kadar Thiamin pada Sampel (mg/Kg)": kadar_mg_kg,
                    "Kadar Thiamin per Tablet (mg/tablet)": kadar_per_tablet
                })
            
            df_sampel_res = pd.DataFrame(results_sampel)
            st.session_state['df_sampel_res'] = df_sampel_res
            
            st.subheader("Hasil Perhitungan Sampel:")
            st.dataframe(df_sampel_res, use_container_width=True)

    # ------------------------------------------
    # FITUR 6: Kontrol Presisi
    # ------------------------------------------
    with tab6:
        st.header("Kontrol Presisi Pengukuran Sampel")
        
        n_ulangan = st.number_input("Ulangan (Jumlah Pengukuran)", min_value=1, max_value=20, value=2, step=1, key="n_presisi")
        
        kadar_list = []
        cols = st.columns(2)
        
        for k in range(int(n_ulangan)):
            with cols[k % 2]:
                val_kadar = st.number_input(f"Kadar Thiamin (mg/Kg) - Ulangan {k+1}", min_value=0.0, value=100.0 + (k*2), format="%.4f", key=f"kadar_p_{k}")
                kadar_list.append(val_kadar)
        
        if len(kadar_list) > 0:
            rerata_kadar = np.mean(kadar_list)
            st.divider()
            st.subheader("Hasil Perhitungan Presisi:")
            
            st.number_input("Rerata Kadar Thiamin (mg/Kg)", value=float(rerata_kadar), format="%.4f", disabled=True)
            
            if len(kadar_kadar := kadar_list) == 2:
                # Hitung %RPD
                selisih = abs(kadar_list[0] - kadar_list[1])
                rpd = (selisih / rerata_kadar) * 100 if rerata_kadar > 0 else 0.0
                
                col_rpd1, col_rpd2 = st.columns(2)
                col_rpd1.number_input("%RPD (Relative Percent Difference)", value=float(rpd), format="%.2f", disabled=True)
                if rpd <= 5.0:
                    col_rpd2.success("Presisi Baik (%RPD ≤ 5%)")
                else:
                    col_rpd2.warning("Presisi Cukup/Kurang (%RPD > 5%)")
                    
            elif len(kadar_list) > 2:
                # Hitung SD dan %RSD
                sd = np.std(kadar_list, ddof=1) # Sample standard deviation
                rsd = (sd / rerata_kadar) * 100 if rerata_kadar > 0 else 0.0
                
                col_sd1, col_sd2, col_sd3 = st.columns(3)
                col_sd1.number_input("Standar Deviasi (SD)", value=float(sd), format="%.4f", disabled=True)
                col_sd2.number_input("%RSD / %KV", value=float(rsd), format="%.2f", disabled=True)
                if rsd <= 2.0:
                    col_sd3.success("Presisi Tinggi (%RSD ≤ 2%)")
                elif rsd <= 5.0:
                    col_sd3.info("Presisi Memenuhi Syarat (%RSD ≤ 5%)")
                else:
                    col_sd3.warning("Presisi Tidak Memenuhi Syarat (%RSD > 5%)")
            else:
                st.info("Masukkan minimal 2 data ulangan untuk menghitung presisi (%RPD atau %RSD).")
