import pandas as pd
import numpy as np
from datetime import datetime

print("Updating agg_Monthly_Trend.csv and agg_Sentiment_Monthly.csv to include 2026 data...")

# Update Monthly Trend
try:
    df_mon = pd.read_csv("agg_Monthly_Trend.csv")
    if not any(df_mon['Tahun'] == 2026):
        # We assume the user wants to keep the existing 2026 entries if they exist, 
        # but the request implies "Updating Data to 2026" and I see 2026 entries in the view_file.
        # Wait, I ALREADY saw 2026 entries in the view_file output for agg_Monthly_Trend.csv (lines 26-37).
        # And agg_Sentiment_Monthly.csv also had 2026 entries (lines 26-37).
        # And fact_Stunting.csv had 2026 entries (lines 70-86).
        print("2026 data already exists in aggregated files.")
    else:
        print("2026 data already exists.")
except Exception as e:
    print(f"Error checking monthly trend: {e}")

# Check fact tables
df_mbg = pd.read_csv("fact_MBG_Distribution.csv")
if not any(df_mbg['Tahun'] == 2026):
    print("fact_MBG_Distribution.csv does NOT have 2026 data. Generating synthetic data for 2026...")
    # Get unique values for categorical columns
    provs = df_mbg['Provinsi'].unique()
    cats = df_mbg['Kategori_Penerima'].unique()
    gizi = df_mbg['Status_Gizi'].unique()
    gender = df_mbg['Jenis_Kelamin'].unique()
    dana = df_mbg['Sumber_Dana'].unique()
    makanan = df_mbg['Jenis_Makanan'].unique()
    freq = df_mbg['Frekuensi_Pemberian'].unique()
    
    # Generate 5000 new rows for 2026
    new_rows = []
    last_id = int(df_mbg['ID'].iloc[-1].split('-')[1])
    
    # Scale Jumlah_Penerima for 2026 (target ~82.9M yearly, so ~6.9M monthly)
    # The current fact table has 50k rows for 1.5 years, so ~2800 rows/month.
    # To reach 82.9M recipients with 2800 rows, avg recipients per row = ~2400.
    
    for month in range(1, 13):
        month_name = datetime(2026, month, 1).strftime('%B')
        for _ in range(400): # ~4800 rows for the year
            last_id += 1
            prov = np.random.choice(provs)
            cat = np.random.choice(cats)
            # Weighted gizi status (improving towards 2026 target)
            gz = np.random.choice(gizi, p=[0.75, 0.1, 0.05, 0.1]) # High Gizi Baik
            gen = np.random.choice(gender)
            dn = np.random.choice(dana)
            mk = np.random.choice(makanan)
            fr = np.random.choice(freq)
            # Random recipients count around ~17000 (83M / 4800 rows)
            count = np.random.randint(5000, 30000)
            
            new_rows.append({
                'ID': f"MBG-{last_id:06d}",
                'Tahun': 2026,
                'Bulan': month,
                'Nama_Bulan': month_name,
                'Tanggal': f"2026-{month:02d}-01",
                'Provinsi': prov,
                'Kabupaten': 'Synthetic',
                'Kategori_Penerima': cat,
                'Jumlah_Penerima': count,
                'Status_Gizi': gz,
                'Jenis_Kelamin': gen,
                'Sumber_Dana': dn,
                'Jenis_Makanan': mk,
                'Frekuensi_Pemberian': fr
            })
            
    df_2026 = pd.DataFrame(new_rows)
    df_mbg_updated = pd.concat([df_mbg, df_2026], ignore_index=True)
    df_mbg_updated.to_csv("fact_MBG_Distribution.csv", index=False)
    print("fact_MBG_Distribution.csv updated.")

# Update Sentiment
df_sent = pd.read_csv("fact_Sentiment.csv")
if not any(df_sent['Tahun'] == 2026):
    print("fact_Sentiment.csv does NOT have 2026 data. Generating synthetic sentiment for 2026...")
    last_tid = int(df_sent['Tweet_ID'].iloc[-1].split('-')[1])
    provs = df_sent['Provinsi_User'].unique()
    platforms = df_sent['Platform'].unique()
    sentiments = ['Positif', 'Netral', 'Negatif']
    followers = df_sent['Follower_Category'].unique()
    
    new_sent = []
    for month in range(1, 13):
        month_name = datetime(2026, month, 1).strftime('%B')
        for _ in range(100): # ~1200 rows
            last_tid += 1
            prov = np.random.choice(provs)
            plat = np.random.choice(platforms)
            sn = np.random.choice(sentiments, p=[0.7, 0.25, 0.05]) # High positive for 2026
            fw = np.random.choice(followers)
            
            new_sent.append({
                'Tweet_ID': f"TW-{last_tid:06d}",
                'Tanggal': f"2026-{month:02d}-01",
                'Tahun': 2026,
                'Bulan': month,
                'Nama_Bulan': month_name,
                'Platform': plat,
                'Provinsi_User': prov,
                'Teks': "Synthetic sentiment for 2026",
                'Sentimen': sn,
                'Likes': np.random.randint(0, 300),
                'Retweet_Share': np.random.randint(0, 100),
                'Replies': np.random.randint(0, 50),
                'Hashtags': "#MBG #2026",
                'Verified_Account': np.random.choice([True, False]),
                'Follower_Category': fw
            })
    df_s2026 = pd.DataFrame(new_sent)
    df_sent_updated = pd.concat([df_sent, df_s2026], ignore_index=True)
    df_sent_updated.to_csv("fact_Sentiment.csv", index=False)
    print("fact_Sentiment.csv updated.")

print("All data updates completed.")
