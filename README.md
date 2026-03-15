# 🍽️ MBG Dashboard — Program Makan Bergizi Gratis

Dashboard analitik interaktif untuk Program Makan Bergizi Gratis (MBG) Indonesia 2024–2025.

**Live:** [mbg-dashboard.streamlit.app](https://mbg-dashboard.streamlit.app)

---

## Fitur

**Executive Overview**
- 5 KPI cards: total penerima, provinsi, stunting, sentimen positif, gizi baik
- Tren distribusi penerima bulanan (Jan 2024 – Jun 2025)
- Breakdown kategori penerima, sumber dana, status gizi, frekuensi pemberian
- Key insights & ranking provinsi

**Regional Insights**
- Horizontal bar chart top 15 provinsi (color-coded stunting level)
- Tabel data lengkap per provinsi
- Bar chart stunting per provinsi vs target nasional 14%
- Distribusi per pulau, scatter penerima vs stunting, capaian target

**Sentiment Analysis**
- 4 KPI sentimen: total, positif, netral, negatif
- Stacked bar tren bulanan + line chart % positif
- 100% proportional bar, distribusi platform, word cloud
- Radar chart dimensi topik, grouped bar per provinsi

---

## Stack

- **Frontend:** Streamlit
- **Charts:** Plotly Express & Graph Objects
- **Data:** 50,000+ rows distribusi MBG + 10,000 sentiment data
- **Fonts:** Instrument Serif + Geist + Geist Mono

---

## Run Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Deploy ke Streamlit Cloud

1. Push repo ini ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` sebagai main file
4. Deploy

---

*by bumimataharisenja*
