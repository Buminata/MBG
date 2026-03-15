import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MBG Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap');

/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'Geist', sans-serif !important;
    color: #1A1A1A;
}
.stApp {
    background-color: #F4F1EA;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Masthead */
.masthead {
    background: #0E0E0E;
    color: #F4F1EA;
    padding: 0 40px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #222;
    font-family: 'Geist Mono', monospace;
    font-size: 11px;
    letter-spacing: .08em;
    text-transform: uppercase;
}
.masthead-center {
    font-family: 'Instrument Serif', serif;
    font-size: 18px;
    letter-spacing: -.01em;
    text-transform: none;
    color: #F4F1EA;
}
.masthead-side { color: #888; }
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #5CDB6A;
    font-size: 10px;
}

/* Hero KPIs */
.hero-strip {
    background: #0E0E0E;
    padding: 40px 40px;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    border-bottom: 1px solid #222;
}
.hero-kpi { padding: 0 28px; border-right: 1px solid #222; }
.hero-kpi:first-child { padding-left: 0; }
.hero-kpi:last-child { border-right: none; }
.hk-label {
    font-family: 'Geist Mono', monospace;
    font-size: 10px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #777;
    margin-bottom: 12px;
}
.hk-val {
    font-family: 'Instrument Serif', serif;
    font-size: 48px;
    line-height: 1;
    letter-spacing: -.02em;
    margin-bottom: 8px;
}
.hk-sub { font-size: 12px; color: #777; }
.hk-delta {
    display: inline-block;
    font-family: 'Geist Mono', monospace;
    font-size: 10px;
    margin-top: 10px;
    padding: 4px 10px;
    border-radius: 4px;
}
.delta-up { background: rgba(92,219,106,.15); color: #5CDB6A; }
.delta-dn { background: rgba(232,85,66,.15); color: #E85542; }

/* Ticker */
.ticker-bar {
    background: #E8E4DC;
    border-bottom: 1px solid #D4CFC4;
    padding: 12px 40px;
    display: flex;
    gap: 40px;
    font-family: 'Geist Mono', monospace;
    font-size: 11px;
    color: #555;
    letter-spacing: .06em;
    overflow-x: auto;
}
.ticker-item { white-space: nowrap; }
.ticker-item strong { color: #1A1A1A; }

/* Section Header */
.sec-header {
    padding: 32px 40px 24px;
    border-top: 2px solid #0E0E0E;
    margin-top: 0;
    display: flex;
    align-items: baseline;
    gap: 20px;
}
.sec-title {
    font-family: 'Instrument Serif', serif;
    font-size: 24px;
    font-weight: 400;
    letter-spacing: -.01em;
}
.sec-num {
    font-family: 'Geist Mono', monospace;
    font-size: 12px;
    color: #888;
}

/* Chart Card */
.chart-card {
    background: #F4F1EA;
    border: 1px solid #D4CFC4;
    padding: 28px;
    height: 100%;
}
.cc-label {
    font-family: 'Instrument Serif', serif;
    font-size: 18px;
    margin-bottom: 6px;
}
.cc-desc {
    font-size: 12px;
    color: #777;
    margin-bottom: 24px;
    line-height: 1.6;
}
.cc-tag {
    display: inline-block;
    font-family: 'Geist Mono', monospace;
    font-size: 9px;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: 3px 8px;
    border: 1px solid #C8C4BA;
    border-radius: 4px;
    color: #888;
    float: right;
    margin-top: -2px;
}

/* Insights strip */
.insights-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    border-top: 1px solid #D4CFC4;
    border-bottom: 1px solid #D4CFC4;
    margin: 0;
}
.insight-box {
    padding: 28px 32px;
    border-right: 1px solid #D4CFC4;
}
.insight-box:last-child { border-right: none; }
.ins-ey {
    font-family: 'Geist Mono', monospace;
    font-size: 9px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 10px;
}
.ins-head {
    font-family: 'Instrument Serif', serif;
    font-size: 16px;
    font-style: italic;
    line-height: 1.5;
    margin-bottom: 10px;
    color: #1A1A1A;
}
.ins-body { font-size: 12px; color: #666; line-height: 1.8; }

/* Sentiment KPI */
.sent-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    border-bottom: 2px solid #0E0E0E;
}
.sent-box {
    padding: 32px 36px;
    border-right: 1px solid #D4CFC4;
}
.sent-box:last-child { border-right: none; }
.sb-label {
    font-family: 'Geist Mono', monospace;
    font-size: 10px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 12px;
}
.sb-num {
    font-family: 'Instrument Serif', serif;
    font-size: 52px;
    line-height: 1;
    letter-spacing: -.02em;
    margin-bottom: 6px;
}
.sb-sub { font-size: 12px; color: #777; }

/* Data Table */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.styled-table thead th {
    text-align: left;
    padding: 12px 16px;
    font-family: 'Geist Mono', monospace;
    font-size: 9px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: #777;
    border-bottom: 2px solid #0E0E0E;
    background: #EDE9E0;
}
.styled-table tbody td {
    padding: 12px 16px;
    border-bottom: 1px solid #E4DFD4;
    vertical-align: middle;
}
.styled-table tbody tr:hover td { background: #EDE9E0; }
.tag-h { color: #C8341A; border: 1px solid #C8341A; border-radius: 4px; padding: 2px 8px; font-size: 10px; font-family: 'Geist Mono', monospace; font-weight: 500; }
.tag-m { color: #B87A10; border: 1px solid #B87A10; border-radius: 4px; padding: 2px 8px; font-size: 10px; font-family: 'Geist Mono', monospace; font-weight: 500; }
.tag-l { color: #1A7A4A; border: 1px solid #1A7A4A; border-radius: 4px; padding: 2px 8px; font-size: 10px; font-family: 'Geist Mono', monospace; font-weight: 500; }

/* Keywords */
.kw-wrap { display: flex; flex-wrap: wrap; gap: 10px; padding: 10px 0; }
.kw-item {
    font-family: 'Geist Mono', monospace;
    border: 1px solid;
    border-radius: 4px;
    padding: 5px 14px;
}

/* Streamlit widget overrides */
.stSelectbox > div > div {
    background: #F4F1EA !important;
    border-color: #C8C4BA !important;
    border-radius: 4px !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 13px !important;
}
.stMultiSelect > div > div {
    background: #F4F1EA !important;
    border-color: #C8C4BA !important;
    border-radius: 4px !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent;
    padding: 0 40px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0 0;
    gap: 0;
    padding-top: 10px;
    padding-bottom: 10px;
    font-family: 'Geist Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .05em;
    color: #888;
}
.stTabs [aria-selected="true"] {
    color: #1A1A1A !important;
    border-bottom-color: #0E0E0E !important;
}

/* Dividers */
hr { border: none; border-top: 1px solid #D4CFC4; margin: 0; }
.thick-hr { border: none; border-top: 2px solid #0E0E0E; margin: 0; }

/* Plotly chart borders */
.js-plotly-plot { border: 1px solid #D4CFC4 !important; }
</style>
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df_mbg   = pd.read_csv("fact_MBG_Distribution.csv")
    df_sent  = pd.read_csv("fact_Sentiment.csv")
    df_stunt = pd.read_csv("fact_Stunting.csv")
    df_prov  = pd.read_csv("agg_By_Province.csv")
    df_mon   = pd.read_csv("agg_Monthly_Trend.csv").sort_values("YearMonth")
    df_smon  = pd.read_csv("agg_Sentiment_Monthly.csv").sort_values("YearMonth")
    df_cat   = pd.read_csv("agg_Category.csv")
    df_dim   = pd.read_csv("dim_Province.csv")
    return df_mbg, df_sent, df_stunt, df_prov, df_mon, df_smon, df_cat, df_dim

df_mbg, df_sent, df_stunt, df_prov, df_mon, df_smon, df_cat, df_dim = load_data()

# ── PLOTLY THEME ─────────────────────────────────────────────────────────────
PAPER   = "#F4F1EA"
PLOT_BG = "#F4F1EA"
GRID    = "#E4DFD4"
INK     = "#1A1A1A"
INK3    = "#888888"
RULE    = "#D4CFC4"

C_BLUE   = "#1A3C8F"
C_RED    = "#C8341A"
C_GREEN  = "#1A7A4A"
C_AMBER  = "#B87A10"
C_SLATE  = "#4A5568"
PALETTE  = [C_BLUE, C_GREEN, C_RED, C_AMBER, C_SLATE,
            "#6B4C9A", "#1A6B7A", "#8B3A2A", "#2A6B4A", "#8B7A1A"]

def base_layout(height=340, legend=True, margin=None):
    m = margin or dict(l=20, r=20, t=20, b=50)
    return dict(
        height=height, paper_bgcolor=PAPER, plot_bgcolor=PLOT_BG,
        font=dict(family="Geist, sans-serif", size=13, color=INK),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28,
                    xanchor="center", x=0.5, font=dict(size=11),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        margin=m,
        xaxis=dict(gridcolor=GRID, linecolor=RULE, tickfont=dict(size=11, color=INK3),
                   zeroline=False, automargin=True),
        yaxis=dict(gridcolor=GRID, linecolor=RULE, tickfont=dict(size=11, color=INK3),
                   zeroline=False, automargin=True),
    )

# ── COMPUTED METRICS ─────────────────────────────────────────────────────────
total_p    = int(df_mbg["Jumlah_Penerima"].sum())
total_prov = int(df_mbg["Provinsi"].nunique())
pct_stunt  = round((df_mbg["Status_Gizi"] == "Stunting").mean() * 100, 1)
pct_gizi   = round((df_mbg["Status_Gizi"] == "Gizi Baik").mean() * 100, 1)
pct_pos    = round((df_sent["Sentimen"] == "Positif").mean() * 100, 1)
pct_neg    = round((df_sent["Sentimen"] == "Negatif").mean() * 100, 1)
pct_net    = round(100 - pct_pos - pct_neg, 1)
total_tw   = len(df_sent)
df_prov_s  = df_prov.sort_values("Total_Penerima", ascending=False).reset_index(drop=True)

# Compute Monthly Growth
df_mon["Growth_Pct"] = df_mon["Total_Penerima"].pct_change() * 100
avg_growth = df_mon["Growth_Pct"].mean()

# ── MASTHEAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <span class="masthead-side">KEMENTERIAN KESEHATAN RI · DATA ANALYTICS</span>
  <span class="masthead-center">Program Makan Bergizi Gratis — Laporan Analitik 2024–2025</span>
  <span class="masthead-side" style="text-align:right;display:flex;gap:20px;align-items:center">
    <span class="live-pill">● LIVE DATA</span>
    <span>50,000+ RECORDS</span>
    <span>17 PROVINSI</span>
  </span>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Executive Overview",
    "Regional Insights",
    "Sentiment Analysis"
])

# ════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════
with tab1:

    # Hero KPI strip
    st.markdown(f"""
    <div class="hero-strip">
      <div class="hero-kpi">
        <div class="hk-label">Total Penerima MBG</div>
        <div class="hk-val" style="color:#5A9EF8">{total_p:,}</div>
        <div class="hk-sub">Jan 2024 – Jun 2025</div>
        <span class="hk-delta delta-up">↑ {avg_growth:.1f}% Avg. MoM</span>
      </div>
      <div class="hero-kpi">
        <div class="hk-label">Provinsi Terjangkau</div>
        <div class="hk-val" style="color:#E8F0FE">{total_prov}</div>
        <div class="hk-sub">dari 38 provinsi nasional</div>
        <span class="hk-delta delta-up">44.7% cakupan wilayah</span>
      </div>
      <div class="hero-kpi">
        <div class="hk-label">Prevalensi Stunting</div>
        <div class="hk-val" style="color:#E85542">{pct_stunt}%</div>
        <div class="hk-sub">Target nasional 2025: 14%</div>
        <span class="hk-delta delta-dn">Gap −2.5% dari target</span>
      </div>
      <div class="hero-kpi">
        <div class="hk-label">Sentimen Positif</div>
        <div class="hk-val" style="color:#5CDB6A">{pct_pos}%</div>
        <div class="hk-sub">dari {total_tw:,} komentar</div>
        <span class="hk-delta delta-up">↑ Naik tiap bulan</span>
      </div>
      <div class="hero-kpi">
        <div class="hk-label">Gizi Baik</div>
        <div class="hk-val" style="color:#E8B842">{pct_gizi}%</div>
        <div class="hk-sub">dari total penerima</div>
        <span class="hk-delta delta-up">Target: 70%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Ticker
    cat_top = df_cat.groupby("Kategori_Penerima")["Total_Penerima"].sum().sort_values(ascending=False)
    st.markdown(f"""
    <div class="ticker-bar">
      <span class="ticker-item">Anak SD <strong>{cat_top.iloc[0]:,}</strong></span>
      <span>·</span>
      <span class="ticker-item">Anak SMP <strong>{cat_top.iloc[1]:,}</strong></span>
      <span>·</span>
      <span class="ticker-item">Balita <strong>{cat_top.iloc[2]:,}</strong></span>
      <span>·</span>
      <span class="ticker-item">Ibu Hamil <strong>{cat_top.iloc[3]:,}</strong></span>
      <span>·</span>
      <span class="ticker-item">Ibu Menyusui <strong>{cat_top.iloc[4]:,}</strong></span>
      <span>·</span>
      <span class="ticker-item">APBN <strong>60%</strong> anggaran</span>
      <span>·</span>
      <span class="ticker-item">NTT stunting tertinggi <strong>33.3%</strong></span>
      <span>·</span>
      <span class="ticker-item">Jawa Barat tertinggi penerima <strong>865K+</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # Insights
    st.markdown("""
    <div class="insights-grid">
      <div class="insight-box">
        <div class="ins-ey">Finding 01</div>
        <div class="ins-head">Pulau Jawa menyerap 55% total penerima nasional</div>
        <div class="ins-body">Tiga provinsi Jawa — Jabar (865K), Jatim (824K), Jateng (767K) — mendominasi distribusi. Ini mencerminkan kepadatan penduduk, bukan efisiensi alokasi per kapita.</div>
      </div>
      <div class="insight-box">
        <div class="ins-ey">Finding 02</div>
        <div class="ins-head">NTT, Papua, NTB butuh intensifikasi mendesak</div>
        <div class="ins-body">Tiga provinsi ini memiliki stunting di atas 27%—jauh melampaui target 14%. Alokasi penerima relatif rendah dibanding tingkat kebutuhan aktual di lapangan.</div>
      </div>
      <div class="insight-box">
        <div class="ins-ey">Finding 03</div>
        <div class="ins-head">Persepsi publik membaik konsisten sejak diluncurkan</div>
        <div class="ins-body">Sentimen positif naik dari 37.2% (Jan 2024) ke 49.1% (Mei 2025), menunjukkan penerimaan masyarakat yang meningkat seiring bertambahnya cakupan dan kualitas program.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Charts row 1: Line + Donut
    st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title">Distribusi & Tren</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="small")

    with col1:
        st.markdown('<div class="chart-card"><div class="cc-label">Tren Penerima per Bulan<span class="cc-tag">Line</span></div><div class="cc-desc">Total penerima bulanan Jan 2024 – Jun 2025 · termasuk MoM growth</div>', unsafe_allow_html=True)
        mon_labels = [str(x)[:7] for x in df_mon["YearMonth"].tolist()]
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=mon_labels, y=df_mon["Total_Penerima"],
            mode="lines+markers",
            line=dict(color=C_BLUE, width=3, shape='spline'),
            marker=dict(size=8, color=C_BLUE, line=dict(color=PAPER, width=2)),
            fill="tozeroy",
            fillcolor="rgba(26,60,143,.08)",
            name="Penerima",
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} penerima<extra></extra>"
        ))
        lo = base_layout(300, legend=False)
        lo["yaxis"]["tickformat"] = ",.0f"
        lo["yaxis"]["title"] = dict(text="Jumlah Penerima", font=dict(size=10, color=INK3))
        fig_line.update_layout(**lo)
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><div class="cc-label">Laju Pertumbuhan MoM (%)<span class="cc-tag">Line</span></div><div class="cc-desc">Perubahan persentase penerima antar bulan</div>', unsafe_allow_html=True)
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(
            x=mon_labels[1:], y=df_mon["Growth_Pct"].iloc[1:],
            mode="lines+markers",
            line=dict(color=C_GREEN, width=3, shape='spline'),
            marker=dict(size=8, color=C_GREEN, line=dict(color=PAPER, width=2)),
            fill="tozeroy",
            fillcolor="rgba(26,122,74,.08)",
            name="Growth Rate",
            hovertemplate="<b>%{x}</b><br>%{y:.2f}%<extra></extra>"
        ))
        fig_growth.add_hline(y=0, line=dict(color=INK, width=1, dash="dot"))
        lo_growth = base_layout(300, legend=False)
        lo_growth["yaxis"]["ticksuffix"] = "%"
        fig_growth.update_layout(**lo_growth)
        st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Charts row 2: Kategori + Dana + Gizi
    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Segmentasi & Sumber Daya</span></div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3, gap="small")

    with col_a:
        st.markdown('<div class="chart-card"><div class="cc-label">Kategori Penerima<span class="cc-tag">Donut</span></div><div class="cc-desc">Proporsi per jenis penerima program MBG</div>', unsafe_allow_html=True)
        cat_agg = df_cat.groupby("Kategori_Penerima")["Total_Penerima"].sum().reset_index().sort_values("Total_Penerima", ascending=False)
        fig_donut = go.Figure(go.Pie(
            labels=cat_agg["Kategori_Penerima"],
            values=cat_agg["Total_Penerima"],
            hole=.55,
            marker=dict(colors=PALETTE[:5], line=dict(color=PAPER, width=2)),
            textinfo="percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>"
        ))
        lo2 = base_layout(280)
        lo2["legend"]["y"] = -0.32
        lo2.pop("xaxis", None); lo2.pop("yaxis", None)
        fig_donut.update_layout(**lo2)
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Charts row 2: Sumber Dana + Gizi + Frekuensi
    col3, col4, col5 = st.columns(3, gap="small")

    with col3:
        st.markdown('<div class="chart-card"><div class="cc-label">Sumber Dana<span class="cc-tag">Bar</span></div><div class="cc-desc">APBN mendominasi 60% total anggaran program</div>', unsafe_allow_html=True)
        sumber = df_mbg.groupby("Sumber_Dana")["Jumlah_Penerima"].sum().reset_index().sort_values("Jumlah_Penerima", ascending=False)
        fig_s = go.Figure(go.Bar(
            x=sumber["Sumber_Dana"], y=sumber["Jumlah_Penerima"],
            marker=dict(color=PALETTE[:4], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} penerima<extra></extra>"
        ))
        lo3 = base_layout(260, legend=False)
        lo3["yaxis"]["tickformat"] = ",.0f"
        lo3["bargap"] = 0.35
        fig_s.update_layout(**lo3)
        st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card"><div class="cc-label">Status Gizi<span class="cc-tag">Donut</span></div><div class="cc-desc">Proporsi kondisi gizi seluruh penerima</div>', unsafe_allow_html=True)
        gizi_data = df_mbg["Status_Gizi"].value_counts().reset_index()
        gizi_data.columns = ["Status", "Count"]
        gizi_colors = {"Gizi Baik": C_GREEN, "Gizi Kurang": C_AMBER, "Stunting": C_RED, "Gizi Lebih": C_BLUE}
        gizi_data["color"] = gizi_data["Status"].map(gizi_colors)
        fig_g = go.Figure(go.Pie(
            labels=gizi_data["Status"], values=gizi_data["Count"],
            hole=.50,
            marker=dict(colors=gizi_data["color"], line=dict(color=PAPER, width=2)),
            textinfo="percent", textfont=dict(size=10),
        ))
        lo4 = base_layout(260)
        lo4["legend"]["y"] = -0.18
        lo4.pop("xaxis", None); lo4.pop("yaxis", None)
        fig_g.update_layout(**lo4)
        st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="chart-card"><div class="cc-label">Frekuensi Pemberian<span class="cc-tag">Pie</span></div><div class="cc-desc">Pola distribusi makanan bergizi per periode</div>', unsafe_allow_html=True)
        frek = df_mbg["Frekuensi_Pemberian"].value_counts().reset_index()
        frek.columns = ["Frekuensi", "Count"]
        fig_f = go.Figure(go.Pie(
            labels=frek["Frekuensi"], values=frek["Count"],
            marker=dict(colors=[C_BLUE, C_SLATE, C_AMBER], line=dict(color=PAPER, width=2)),
            textinfo="percent+label", textfont=dict(size=10),
        ))
        lo5 = base_layout(260, legend=False)
        lo5.pop("xaxis", None); lo5.pop("yaxis", None)
        fig_f.update_layout(**lo5)
        st.plotly_chart(fig_f, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Top 5 progress
    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Ranking Provinsi</span></div>', unsafe_allow_html=True)
    col6, col7 = st.columns(2, gap="small")

    with col6:
        st.markdown('<div class="chart-card"><div class="cc-label">Top 5 — Total Penerima</div><div class="cc-desc">Proporsi terhadap total nasional 5.1 juta</div>', unsafe_allow_html=True)
        top5 = df_prov_s.head(5)
        for _, row in top5.iterrows():
            pct = row["Total_Penerima"] / total_p * 100
            st.markdown(f"""
            <div class="prog-item" style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
              <span style="font-size:11px;color:#3A3A3A;width:130px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{row['Provinsi']}</span>
              <div style="flex:1;height:5px;background:#E4DFD4;border-radius:0">
                <div style="width:{pct:.0f}%;height:100%;background:{C_BLUE}"></div>
              </div>
              <span style="font-family:'Geist Mono',monospace;font-size:10px;color:#888;width:52px;text-align:right">{row['Total_Penerima']/1000:.0f}K</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col7:
        st.markdown('<div class="chart-card"><div class="cc-label">Top 5 — Stunting Tertinggi</div><div class="cc-desc">Provinsi prioritas intervensi program gizi</div>', unsafe_allow_html=True)
        stunt_sorted = df_prov_s.nlargest(5, "Prevalensi_Stunting_Pct")
        for _, row in stunt_sorted.iterrows():
            pct = row["Prevalensi_Stunting_Pct"]
            c = C_RED if pct > 25 else C_AMBER if pct > 18 else C_GREEN
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
              <span style="font-size:11px;color:#3A3A3A;width:130px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{row['Provinsi']}</span>
              <div style="flex:1;height:5px;background:#E4DFD4;border-radius:0">
                <div style="width:{pct/45*100:.0f}%;height:100%;background:{c}"></div>
              </div>
              <span style="font-family:'Geist Mono',monospace;font-size:10px;color:{c};width:52px;text-align:right">{pct:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 2 — REGIONAL INSIGHTS
# ════════════════════════════════════════════════════════
with tab2:

    st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title">Distribusi per Provinsi</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="small")

    with col1:
        st.markdown('<div class="chart-card"><div class="cc-label">Top 15 Provinsi — Total Penerima MBG<span class="cc-tag">H-Bar</span></div><div class="cc-desc">Warna menunjukkan tingkat prevalensi stunting: merah = tinggi, kuning = sedang, hijau = rendah</div>', unsafe_allow_html=True)
        color_map = {"Tinggi (>25%)": C_RED, "Sedang (18-25%)": C_AMBER, "Rendah (<18%)": C_GREEN}
        df_prov_plot = df_prov_s.head(15).copy()
        df_prov_plot["color"] = df_prov_plot["Stunting_Label"].map(color_map)
        fig_hbar = go.Figure(go.Bar(
            y=df_prov_plot["Provinsi"][::-1],
            x=df_prov_plot["Total_Penerima"][::-1],
            orientation="h",
            marker=dict(color=df_prov_plot["color"][::-1], line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f} penerima<extra></extra>"
        ))
        lo = base_layout(420, legend=False)
        lo["xaxis"]["tickformat"] = ",.0f"
        lo["xaxis"]["title"] = dict(text="Total Penerima", font=dict(size=10, color=INK3))
        lo["bargap"] = 0.25
        fig_hbar.update_layout(**lo)
        st.plotly_chart(fig_hbar, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card" style="overflow:hidden"><div class="cc-label">Ranking Provinsi Lengkap</div><div class="cc-desc">Data penerima & status stunting 2024</div>', unsafe_allow_html=True)
        rows_html = ""
        for i, row in df_prov_s.iterrows():
            sl = str(row.get("Stunting_Label", ""))
            tag = "tag-h" if "Tinggi" in sl else "tag-m" if "Sedang" in sl else "tag-l"
            label = "TINGGI" if "Tinggi" in sl else "SEDANG" if "Sedang" in sl else "RENDAH"
            rank_class = "gold" if i == 0 else "silver" if i == 1 else "bronze" if i == 2 else ""
            rank_style = f"color:{'#B87A10' if rank_class=='gold' else '#4A5568' if rank_class=='silver' else '#9A6030' if rank_class=='bronze' else '#888'};font-weight:{'600' if rank_class else '400'}"
            w = int(row["Total_Penerima"] / df_prov_s["Total_Penerima"].max() * 80)
            rows_html += f"""<tr>
              <td><span style="font-family:'Geist Mono',monospace;font-size:11px;{rank_style}">{i+1:02d}</span></td>
              <td style="font-weight:500;font-size:12px">{row['Provinsi']}</td>
              <td>
                <span style="font-family:'Geist Mono',monospace;font-size:11px">{int(row['Total_Penerima']):,}</span>
                <div style="height:3px;background:#E4DFD4;width:80px;margin-top:3px">
                  <div style="height:100%;width:{w}px;background:{C_BLUE}"></div>
                </div>
              </td>
              <td><span style="font-family:'Geist Mono',monospace;font-size:11px;color:{'#C8341A' if 'Tinggi' in sl else '#B87A10' if 'Sedang' in sl else '#1A7A4A'}">{row['Prevalensi_Stunting_Pct']:.1f}%</span></td>
              <td><span class="{tag}">{label}</span></td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-y:auto;max-height:400px">
          <table class="styled-table">
            <thead><tr><th>#</th><th>Provinsi</th><th>Penerima</th><th>Stunting</th><th>Level</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Stunting full bar
    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Prevalensi Stunting 2024</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="cc-label">% Stunting per Provinsi vs Target Nasional 14%<span class="cc-tag">Bar + Target</span></div><div class="cc-desc">Garis biru = target nasional 2025 · merah = sangat prioritas · oranye = perlu perhatian · hijau = relatif baik</div>', unsafe_allow_html=True)

    stunt24 = df_stunt[df_stunt["Tahun"] == 2024].sort_values("Prevalensi_Stunting_Pct", ascending=False)
    bar_colors = [C_RED if v > 25 else C_AMBER if v > 18 else C_GREEN for v in stunt24["Prevalensi_Stunting_Pct"]]
    fig_stunt = go.Figure()
    fig_stunt.add_trace(go.Bar(
        x=stunt24["Provinsi"], y=stunt24["Prevalensi_Stunting_Pct"],
        marker=dict(color=bar_colors, line=dict(width=0)),
        name="% Stunting",
        hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"
    ))
    fig_stunt.add_hline(y=14, line=dict(color=C_BLUE, width=1.5, dash="dash"),
                        annotation_text="Target 14%", annotation_position="right",
                        annotation_font=dict(size=10, color=C_BLUE))
    lo_s = base_layout(280, legend=False)
    lo_s["yaxis"]["title"] = dict(text="% Stunting", font=dict(size=10, color=INK3))
    lo_s["xaxis"]["tickangle"] = -35
    lo_s["xaxis"]["tickfont"] = dict(size=10)
    fig_stunt.update_layout(**lo_s)
    st.plotly_chart(fig_stunt, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Pulau + Scatter
    col3, col4, col5 = st.columns(3, gap="small")

    with col3:
        st.markdown('<div class="chart-card"><div class="cc-label">Distribusi per Pulau<span class="cc-tag">Donut</span></div><div class="cc-desc">Sebaran geografis penerima MBG nasional</div>', unsafe_allow_html=True)
        pulau_data = {"Jawa": 2810153, "Sumatera": 976067, "Kalimantan": 301824, "Sulawesi": 254592, "Bali & NT": 458708, "Papua": 108289}
        fig_p = go.Figure(go.Pie(
            labels=list(pulau_data.keys()), values=list(pulau_data.values()),
            hole=.48,
            marker=dict(colors=PALETTE[:6], line=dict(color=PAPER, width=2)),
            textinfo="percent", textfont=dict(size=10),
        ))
        lo6 = base_layout(280)
        lo6["legend"]["y"] = -0.22
        lo6.pop("xaxis", None); lo6.pop("yaxis", None)
        fig_p.update_layout(**lo6)
        st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card"><div class="cc-label">Scatter: Penerima vs Stunting<span class="cc-tag">Scatter</span></div><div class="cc-desc">Korelasi antara jumlah penerima dan tingkat stunting per provinsi</div>', unsafe_allow_html=True)
        sc_colors = [C_RED if s > 25 else C_AMBER if s > 18 else C_GREEN for s in df_prov_s["Prevalensi_Stunting_Pct"]]
        fig_sc = go.Figure(go.Scatter(
            x=df_prov_s["Total_Penerima"] / 1000,
            y=df_prov_s["Prevalensi_Stunting_Pct"],
            mode="markers+text",
            text=df_prov_s["Provinsi"].str[:4],
            textposition="top center",
            textfont=dict(size=8, color=INK3),
            marker=dict(size=10, color=sc_colors, line=dict(color=PAPER, width=1.5)),
            hovertemplate="<b>%{text}</b><br>%{x:.0f}K penerima<br>%{y:.1f}% stunting<extra></extra>"
        ))
        lo7 = base_layout(280, legend=False)
        lo7["xaxis"]["title"] = dict(text="Penerima (ribu)", font=dict(size=10, color=INK3))
        lo7["yaxis"]["title"] = dict(text="% Stunting", font=dict(size=10, color=INK3))
        fig_sc.update_layout(**lo7)
        st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="chart-card"><div class="cc-label">Status Capaian Target<span class="cc-tag">Donut</span></div><div class="cc-desc">Provinsi yang sudah / belum capai target stunting &lt;18%</div>', unsafe_allow_html=True)
        tercapai = int((df_prov_s["Prevalensi_Stunting_Pct"] < 18).sum())
        proses = len(df_prov_s) - tercapai
        fig_t = go.Figure(go.Pie(
            labels=["Di bawah target", "Masih di atas target"],
            values=[tercapai, proses], hole=.55,
            marker=dict(colors=[C_GREEN, C_AMBER], line=dict(color=PAPER, width=2)),
            textinfo="value+percent", textfont=dict(size=11),
        ))
        lo8 = base_layout(280)
        lo8["legend"]["y"] = -0.18
        lo8.pop("xaxis", None); lo8.pop("yaxis", None)
        fig_t.update_layout(**lo8)
        st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# PAGE 3 — SENTIMENT ANALYSIS
# ════════════════════════════════════════════════════════
with tab3:

    # Sentiment KPI strip
    st.markdown(f"""
    <div class="sent-grid">
      <div class="sent-box">
        <div class="sb-label">Total Komentar</div>
        <div class="sb-num" style="color:{C_BLUE}">{total_tw:,}</div>
        <div class="sb-sub">5 platform · Jan 2024–Jun 2025</div>
      </div>
      <div class="sent-box">
        <div class="sb-label">Sentimen Positif</div>
        <div class="sb-num" style="color:{C_GREEN}">{pct_pos}%</div>
        <div class="sb-sub">4,275 komentar · tren naik</div>
      </div>
      <div class="sent-box">
        <div class="sb-label">Sentimen Netral</div>
        <div class="sb-num" style="color:{C_AMBER}">{pct_net}%</div>
        <div class="sb-sub">3,603 komentar</div>
      </div>
      <div class="sent-box">
        <div class="sb-label">Sentimen Negatif</div>
        <div class="sb-num" style="color:{C_RED}">{pct_neg}%</div>
        <div class="sb-sub">2,122 komentar · tren turun</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-header"><span class="sec-num">01</span><span class="sec-title">Tren Sentimen Publik</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.markdown('<div class="chart-card"><div class="cc-label">Volume Sentimen per Bulan<span class="cc-tag">Stacked Bar</span></div><div class="cc-desc">Distribusi komentar Positif / Netral / Negatif setiap bulan</div>', unsafe_allow_html=True)
        s_labels = [str(x)[:7] for x in df_smon["YearMonth"].tolist()]
        fig_sb = go.Figure()
        for col_name, color, label in [("Positif", C_GREEN, "Positif"), ("Netral", C_AMBER, "Netral"), ("Negatif", C_RED, "Negatif")]:
            if col_name in df_smon.columns:
                fig_sb.add_trace(go.Bar(
                    name=label, x=s_labels, y=df_smon[col_name],
                    marker=dict(color=color, line=dict(width=0)),
                    hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y}} komentar<extra></extra>"
                ))
        lo9 = base_layout(300)
        lo9["barmode"] = "stack"
        lo9["legend"]["y"] = -0.22
        fig_sb.update_layout(**lo9)
        st.plotly_chart(fig_sb, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card"><div class="cc-label">Tren % Sentimen Positif<span class="cc-tag">Line</span></div><div class="cc-desc">Persentase komentar positif per bulan — naik dari 37% ke 49%</div>', unsafe_allow_html=True)
        pct_col = "Pct_Positif" if "Pct_Positif" in df_smon.columns else None
        if pct_col:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=s_labels, y=df_smon[pct_col],
                mode="lines+markers",
                line=dict(color=C_GREEN, width=3, shape='spline'),
                marker=dict(size=8, color=C_GREEN, line=dict(color=PAPER, width=2)),
                fill="tozeroy", fillcolor="rgba(26,122,74,.08)",
                name="% Positif",
                hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"
            ))
            fig_trend.add_hline(y=50, line=dict(color=INK, width=1, dash="dot"),
                                annotation_text="Target 50%", annotation_font=dict(size=11, color=INK3))
            lo10 = base_layout(300, legend=False)
            lo10["yaxis"]["ticksuffix"] = "%"
            lo10["yaxis"]["range"] = [30, 55]
            fig_trend.update_layout(**lo10)
            st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # 100% Stacked + Platform + Keywords
    col3, col4, col5 = st.columns(3, gap="small")

    with col3:
        st.markdown('<div class="chart-card"><div class="cc-label">100% Proporsi Sentimen<span class="cc-tag">100% Bar</span></div><div class="cc-desc">Pergeseran proporsi relatif per bulan</div>', unsafe_allow_html=True)
        if all(c in df_smon.columns for c in ["Positif","Netral","Negatif"]):
            tots = df_smon["Positif"] + df_smon["Netral"] + df_smon["Negatif"]
            fig_pct = go.Figure()
            for col_name, color, label in [("Positif",C_GREEN,"Positif"),("Netral",C_AMBER,"Netral"),("Negatif",C_RED,"Negatif")]:
                fig_pct.add_trace(go.Bar(
                    name=label, x=s_labels, y=(df_smon[col_name]/tots*100).round(1),
                    marker=dict(color=color, line=dict(width=0)),
                ))
            lo11 = base_layout(260)
            lo11["barmode"] = "stack"
            lo11["yaxis"]["ticksuffix"] = "%"
            lo11["yaxis"]["range"] = [0, 100]
            lo11["legend"]["y"] = -0.26
            fig_pct.update_layout(**lo11)
            st.plotly_chart(fig_pct, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card"><div class="cc-label">Distribusi Platform<span class="cc-tag">Bar</span></div><div class="cc-desc">Volume komentar per platform media sosial</div>', unsafe_allow_html=True)
        plat = df_sent["Platform"].value_counts().reset_index()
        plat.columns = ["Platform", "Count"]
        fig_plat = go.Figure(go.Bar(
            x=plat["Platform"], y=plat["Count"],
            marker=dict(color=PALETTE[:5], line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>%{y:,} komentar<extra></extra>"
        ))
        lo12 = base_layout(260, legend=False)
        lo12["bargap"] = 0.35
        fig_plat.update_layout(**lo12)
        st.plotly_chart(fig_plat, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="chart-card"><div class="cc-label">Kata Kunci Dominan<span class="cc-tag">Word Cloud</span></div><div class="cc-desc">Frekuensi kemunculan dalam seluruh komentar</div>', unsafe_allow_html=True)
        kws = [
            ("bergizi", 4821, C_BLUE, 18),("gratis", 4105, C_GREEN, 17),
            ("stunting", 3892, C_RED, 16),("anak", 3654, C_BLUE, 15),
            ("distribusi", 2987, C_AMBER, 14),("gizi", 2876, C_GREEN, 14),
            ("balita", 2541, C_BLUE, 13),("terlambat", 1923, C_RED, 13),
            ("pemerintah", 1876, C_SLATE, 12),("sehat", 1754, C_GREEN, 12),
            ("posyandu", 1623, "#6B4C9A", 12),("manfaat", 1287, C_GREEN, 11),
            ("#MBG", 1398, C_BLUE, 13),("anggaran", 1432, C_RED, 12),
            ("ibu", 1156, C_AMBER, 11),
        ]
        kw_html = '<div class="kw-wrap">'
        for w, f, c, s in kws:
            bg = c + "15"
            kw_html += f'<span class="kw-item" style="font-size:{s}px;color:{c};border-color:{c}30;background:{bg}" title="Frekuensi: {f:,}">{w}</span>'
        kw_html += '</div>'
        st.markdown(kw_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Radar
    st.markdown('<div class="sec-header"><span class="sec-num">02</span><span class="sec-title">Analisis Mendalam</span></div>', unsafe_allow_html=True)
    col6, col7 = st.columns(2, gap="small")

    with col6:
        st.markdown('<div class="chart-card"><div class="cc-label">Radar — Dimensi Topik Sentimen<span class="cc-tag">Radar</span></div><div class="cc-desc">Perbandingan sentimen positif vs negatif per dimensi topik pembahasan</div>', unsafe_allow_html=True)
        cats_r = ["Distribusi","Kualitas","Dampak Gizi","Transparansi","Aksesibilitas","Kecepatan"]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=[75,60,80,55,70,50], theta=cats_r, fill="toself", name="Positif",
            line=dict(color=C_GREEN, width=2),
            fillcolor="rgba(26,122,74,.12)"
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=[40,55,35,65,45,60], theta=cats_r, fill="toself", name="Negatif",
            line=dict(color=C_RED, width=2),
            fillcolor="rgba(200,52,26,.08)"
        ))
        fig_r.update_layout(
            height=300, paper_bgcolor=PAPER, plot_bgcolor=PAPER,
            font=dict(family="Geist", size=10, color=INK),
            margin=dict(l=40, r=40, t=20, b=20),
            polar=dict(
                bgcolor=PAPER,
                radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=9, color=INK3), gridcolor=GRID, linecolor=RULE),
                angularaxis=dict(tickfont=dict(size=10, color=INK2 if False else "#3A3A3A"), gridcolor=GRID, linecolor=RULE)
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, xanchor="center", x=.5, font=dict(size=10))
        )
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col7:
        st.markdown('<div class="chart-card"><div class="cc-label">Sentimen per Provinsi Top 10<span class="cc-tag">Grouped Bar</span></div><div class="cc-desc">Perbandingan volume sentimen positif vs negatif antar provinsi</div>', unsafe_allow_html=True)
        sent_prov = df_sent.groupby(["Provinsi_User","Sentimen"]).size().unstack(fill_value=0).reset_index()
        for c in ["Positif","Netral","Negatif"]:
            if c not in sent_prov.columns:
                sent_prov[c] = 0
        sent_prov = sent_prov.nlargest(10, "Positif")
        fig_gbar = go.Figure()
        fig_gbar.add_trace(go.Bar(name="Positif", x=sent_prov["Provinsi_User"], y=sent_prov["Positif"],
                                   marker=dict(color=C_GREEN, line=dict(width=0))))
        fig_gbar.add_trace(go.Bar(name="Negatif", x=sent_prov["Provinsi_User"], y=sent_prov["Negatif"],
                                   marker=dict(color=C_RED, line=dict(width=0))))
        lo13 = base_layout(300)
        lo13["barmode"] = "group"
        lo13["bargap"] = 0.3
        lo13["xaxis"]["tickangle"] = -35
        lo13["xaxis"]["tickfont"] = dict(size=10)
        fig_gbar.update_layout(**lo13)
        st.plotly_chart(fig_gbar, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0E0E0E;color:#555;padding:20px 40px;
  display:flex;justify-content:space-between;align-items:center;
  font-family:'Geist Mono',monospace;font-size:10px;letter-spacing:.06em;margin-top:40px">
  <span>MBG DASHBOARD · DATA ANALITIK PROGRAM GIZI NASIONAL · 2024–2025</span>
  <span style="color:#F4F1EA;font-family:'Instrument Serif',serif;font-style:italic;font-size:13px">bumimataharisenja</span>
  <span>BUILT WITH STREAMLIT & PLOTLY · 50,000+ RECORDS</span>
</div>
""", unsafe_allow_html=True)
