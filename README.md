# Simulasi Perilaku Pembelian Pelanggan pada E-Commerce dengan Agent-Based Modeling (ABM)

## Identitas Proyek Akademik
- **Nama Mahasiswa:** Muhammad Iqbal Fadel
- **NIM:** 202310370311268
- **Mata Kuliah:** Pemodelan dan Simulasi Data
- **Kelas:** D
- **Dosen Pengampu:** Vinna Rahmayanti S, S.Si., M.Si.
- **Topik Proyek:** Agent-Based Modeling (ABM) untuk Simulasi Perilaku Pembelian Pelanggan pada E-Commerce

---

## Deskripsi Singkat
Proyek ini mengimplementasikan sistem simulasi berbasis agen (Agent-Based Modeling) untuk memodelkan perilaku pembelian pelanggan dalam lingkungan e-commerce. Simulasi ini bertujuan untuk menganalisis bagaimana berbagai variabel, seperti tingkat diskon, minat pelanggan, dan suasana hati (shopping mood), memengaruhi agregat volume transaksi. Proyek ini disusun sebagai pemenuhan Tugas Akhir praktikum mata kuliah Pemodelan dan Simulasi Data semester 6.

## Latar Belakang
Dalam ekosistem e-commerce, perilaku pembelian pelanggan adalah faktor kunci dalam mengoptimalkan strategi penjualan. Namun, perilaku konsumen secara agregat tidak sekadar akumulasi dari individu yang identik, melainkan hasil interaksi dinamis dari berbagai faktor kognitif dan situasional masing-masing pelanggan.

Pendekatan Agent-Based Modeling (ABM) sangat relevan untuk memodelkan sistem yang kompleks ini. Dengan merepresentasikan setiap pelanggan sebagai agen otonom yang memiliki aturan pengambilan keputusannya sendiri, kita dapat mengamati pola perilaku kolektif yang muncul secara natural dari interaksi agen dengan lingkungannya, tanpa perlu mendefinisikan aturan makro secara kaku.

## Tujuan Simulasi
1. Mengimplementasikan model matematika probabilitas dalam logika keputusan agen pelanggan.
2. Mensimulasikan dan mengukur dampak tingkat diskon (Discount Rate) terhadap probabilitas pembelian.
3. Membandingkan volume transaksi penjualan pada berbagai kondisi emosional pelanggan (Shopping Mood) melalui perulangan simulasi stokastik (Monte Carlo).

## Metode yang Digunakan

### 1. Agent-Based Modeling (ABM)
ABM digunakan untuk memodelkan pelanggan secara individu (mikro) dengan sekumpulan atribut dan aturan keputusan (rules). Hal ini memungkinkan kita melihat fenomena emergent (makro) berupa total transaksi berdasarkan variasi kondisi lingkungan.

### 2. Monte Carlo Simulation
Karena pengambilan keputusan pembelian pada tingkat agen bersifat stokastik (memanfaatkan generasi nilai acak), simulasi ini menggunakan metode Monte Carlo. Metode ini bekerja dengan melakukan perulangan (iterasi) dalam jumlah besar untuk menghasilkan distribusi agregat yang stabil dan mendekati nilai probabilitas teoretis (konvergensi data).

---

## Struktur Agent dan Variabel Simulasi

### Atribut Agent (Pelanggan)
Setiap agen dalam simulasi diinisialisasi dengan atribut independen berikut:
- **Purchase Probability (P):** Probabilitas dasar (baseline) pelanggan untuk melakukan pembelian [0.1 - 0.5].
- **Interest Level (I):** Tingkat ketertarikan pelanggan terhadap produk [0.0 - 1.0].
- **Budget (B):** Anggaran maksimal yang dimiliki pelanggan [50 - 500].
- **Shopping Mood (M):** Faktor emosional/suasana hati pelanggan [0.0 - 1.0].

### Variabel Lingkungan
- **Product Price:** Harga produk tetap senilai 100 unit.
- **Discount Rate:** Tingkat potongan harga yang diberikan kepada seluruh agen [0% - 50%].
- **Jumlah Agent:** Jumlah agen (pelanggan) yang berpartisipasi dalam sistem [10 - 500].
- **Jumlah Iterasi:** Banyaknya siklus Monte Carlo yang dijalankan [100 - 5000].

## Formulasi Model

Model pengambilan keputusan agen dihitung menggunakan formula probabilitas sebagai berikut:

`P_final = min(P + (I × discount) + (M × 0.2), 1.0)`

**Keterangan:**
- `P_final` adalah probabilitas akhir agen untuk melakukan pembelian.
- Nilai akhir dibatasi (clipped) pada angka maksimal 1.0 (100% peluang membeli).
- Keputusan pembelian akhir *(buy/not buy)* divalidasi dengan dua syarat:
  1. Pelanggan harus memiliki uang yang cukup: `Budget >= (Product Price × (1 - discount))`.
  2. Nilai acak yang digenerasi `random.random()` harus lebih kecil dari `P_final`.

---

## Struktur Folder Project

```text
PEMODELAN_DAN_SIMULASI_DATA/
│
├── Main.ipynb              # Notebook Python berisi perumusan logika dan analisis eksplorasi data
├── app.py                  # Skrip utama Dashboard Streamlit interaktif
├── requirements.txt        # Daftar dependensi pustaka Python
├── README.md               # Dokumentasi utama repositori
└── Reports/                # Laporan perkembangan berkala
    ├── MINGGU 2.docx       # Laporan Konseptualisasi
    ├── MINGGU 4.docx       # Laporan Perencanaan (Fase 1)
    ├── MINGGU 6.docx       # Laporan Awal Implementasi
    ├── MINGGU 8.docx       # Laporan Skenario Dasar
    ├── MINGGU 10.docx      # Laporan Shopping Mood
    └── MINGGU 12.docx      # Laporan Monte Carlo
```

---

## Cara Menjalankan Program

### Prasyarat Instalasi
Pastikan sistem operasi Anda telah memiliki Python versi 3.7 ke atas. Unduh atau clone repositori ini ke dalam sistem Anda. Disarankan untuk menggunakan virtual environment.

Jalankan perintah berikut pada terminal untuk menginstal pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### Cara Menjalankan Dashboard Streamlit
Aplikasi utama adalah antarmuka web interaktif yang dikembangkan menggunakan pustaka Streamlit.
1. Buka terminal atau Command Prompt.
2. Arahkan direktori (cd) ke dalam folder repositori ini.
3. Jalankan perintah:
```bash
streamlit run app.py
```
4. Sistem secara otomatis akan membuka peramban web (browser) pada alamat `http://localhost:8501`.

### Penggunaan Dashboard
- Gunakan area pengaturan (Sidebar) untuk menyesuaikan nilai **Discount Rate**, **Shopping Mood**, **Jumlah Agent**, dan **Jumlah Iterasi**.
- Klik tombol **"Jalankan Simulasi"** untuk melakukan kalkulasi simulasi Monte Carlo.
- Hasil keluaran dapat dianalisis pada panel *Metric Cards*, *Grafik Monte Carlo*, dan *Ringkasan Hasil*.

---

## Hasil Simulasi
Eksekusi model simulasi ini memberikan gambaran kuantitatif mengenai perilaku agen. Beberapa temuan utama dari simulasi ini antara lain:
1. **Dampak Potongan Harga:** Terdapat hubungan berbanding lurus antara peningkatan persentase diskon dengan kenaikan jumlah rata-rata transaksi harian, yang disebabkan oleh naiknya probabilitas beli setiap agen.
2. **Volatilitas Suasana Hati:** Pergeseran nilai kondisi emosional agregat *(Shopping mood)* dari rendah ke tinggi dapat secara signifikan meningkatkan frekuensi transaksi pada kondisi harga yang konstan.
3. **Kestabilan Statistik:** Sesuai prinsip Monte Carlo, meningkatkan jumlah iterasi dapat menyempitkan variansi sehingga fluktuasi grafik simulasi antar siklus cenderung lebih dapat diprediksi.

---

## Keterbatasan Model
Simulasi ini dirancang untuk tujuan akademik dengan batasan sebagai berikut:
1. **Penggunaan Nilai Acak:** Parameter bawaan setiap agen dihasilkan menggunakan distribusi probabilitas acak (*Uniform Distribution*), bukan bersumber dari dataset transaksi pelanggan riil.
2. **Tidak Ada Dinamika Waktu:** Model dijalankan sebagai abstraksi kejadian tunggal (*snapshot*). Model tidak mempertimbangkan interaksi berulang pelanggan dari waktu ke waktu, faktor musiman, atau pergeseran tren.
3. **Tanpa Pengaruh Sosial Eksternal:** Model belum mempertimbangkan efek interaksi antar agen (misalnya sentimen pasar, ulasan, atau *word-of-mouth*). Keputusan pembelian masing-masing agen bersifat terisolasi.
4. **Fokus Implementasi:** Simulasi ini bertujuan untuk mengeksplorasi konsep pemodelan data, bukan ditujukan sebagai alat bantu analitik bisnis maupun prediksi penjualan untuk pasar nyata.

---

## Kesimpulan
Melalui integrasi Agent-Based Modeling dan metode Monte Carlo, proyek ini berhasil mensimulasikan bagaimana variabel tingkat mikro (probabilitas dasar, ketersediaan anggaran, tingkat diskon, dan suasana hati) berinteraksi dan membentuk pola transaksi secara makro. Dashboard Streamlit interaktif yang dibangun juga mempermudah pengujian berbagai skenario eksperimen secara fleksibel dan visual.
