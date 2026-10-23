# 🧪 Kalkulator Perhitungan Kadar Thiamin (UV-Vis)

Aplikasi berbasis web menggunakan **Streamlit** untuk mempermudah perhitungan laboratorium dalam penentuan kadar Thiamin (Vitamin B1) menggunakan metode Spektrofotometri UV-Vis.

## 🚀 Fitur Utama

1. **Pembuatan Larutan Induk Thiamin**: Menghitung bobot sampel standar murni (gram) yang harus ditimbang.
2. **Pembuatan Larutan Standar Thiamin**: Menghitung volume pengenceran dari larutan induk.
3. **Pembuatan Deret Standar Thiamin**: Fitur dinamis untuk menghitung volume pemipetan larutan standar untuk berbagai variasi konsentrasi.
4. **Data Hasil Pengujian**: Melakukan analisis regresi linier otomatis ($y = bx + a$) untuk mendapatkan nilai *slope*, *intercept*, $r$, dan $R^2$ disertai grafik kurva kalibrasi.
5. **Perhitungan Konsentrasi Sampel**: Menghitung konsentrasi terukur (mg/L), kadar thiamin pada sampel (mg/kg), dan kadar thiamin per tablet (mg/tablet).
6. **Kontrol Presisi**: Menghitung nilai %RPD (untuk 2 ulangan) atau Standar Deviasi & %RSD (untuk >2 ulangan).

## 🛠️ Cara Menjalankan secara Lokal

1. **Clone repository ini**:
   ```bash
   git clone [https://github.com/davinafaizaa/kalkulator-thiamin.git](https://github.com/username/kalkulator-thiamin.git)
   cd kalkulator-thiamin
   python -m venv venv
