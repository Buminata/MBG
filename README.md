# 🍽️ MBG Dashboard — Program Makan Bergizi Gratis

Dashboard analitik interaktif untuk Program Makan Bergizi Gratis (MBG) Indonesia periode **2024–2026**.

**Live:** [mbg-dashboard.streamlit.app](https://mbg-dashboard.streamlit.app)

---

## Fitur Utama

### 📊 Executive Overview

- **5 KPI Utama**: Total penerima (80M+), cakupan provinsi, prevalensi stunting, sentimen publik, dan status gizi baik.
- **Tren Bulanan**: Visualisasi pertumbuhan penerima dari Januari 2024 hingga **Desember 2026**.
- **Analisis Kategori**: Breakdown berdasarkan kategori penerima, sumber dana, dan status gizi.

### 🗺️ Regional Insights

- **Top 15 Provinsi**: Grafik batang horizontal dengan kode warna tingkat stunting.
- **Peta Distribusi**: Analisis per pulau dan korelasi jumlah penerima terhadap target stunting nasional (14%).
- **Capaian Target**: Monitoring progres setiap wilayah terhadap parameter keberhasilan program.

### 🎭 Sentiment Analysis

- **KPI Sentimen**: Monitoring volume komentar positif, netral, dan negatif di 5 platform utama.
- **Tren Sentimen**: Proyeksi pertumbuhan sentimen positif hingga 71% di tahun 2026.
- **NLP Visuals**: Word Cloud dan Radar Chart untuk dimensi topik pembicaraan publik.

### 🚀 Strategic Roadmap 2026 (New)

- **Proyeksi Anggaran**: Visualisasi peningkatan anggaran dari Rp 6.7T (2024) ke Rp 335T (2026).
- **Target Penerima**: Skalabilitas program menuju target 82.9 Juta penerima.
- **Workforce Expansion**: Penyerapan tenaga kerja nasional hingga 1.55 Juta orang melalui SPPG.
- **Unit Pelayanan**: Pembangunan 33,000 unit Satuan Pelayanan Makan Bergizi (SPPG).

---

## Tech Stack

- **Framework:** Streamlit
- **Visualisasi:** Plotly Express & Graph Objects
- **Pengolahan Data:** Pandas & NumPy
- **Runtime:** Python 3.14 (Optimized for Streamlit Cloud)
- **Tipografi:** Google Fonts (Instrument Serif, Geist, Geist Mono)

---

## Pengembangan Lokal

1. Clone repositori ini
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python -m streamlit run app.py
   ```

---

## Deploy ke Streamlit Cloud

1. Push pembaruan kode ke branch `main`.
2. Pastikan file `runtime.txt` berisi `python-3.14`.
3. Gunakan **Advanced Settings** di dashboard Streamlit Cloud untuk memastikan koneksi repositori aktif.

---

_Created by Buminata Research & Development_
