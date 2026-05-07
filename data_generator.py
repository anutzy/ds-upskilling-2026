"""Generator dataset vânzări retail RO pentru exerciții Pandas."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)

n = 50_000
orase = ['București', 'Cluj', 'Iași', 'Timișoara', 'Constanța', 'Brașov', 'Craiova']
categorii = ['Electronice', 'Îmbrăcăminte', 'Alimente', 'Casă', 'Cosmetice', 'Sport']
canal = ['Online', 'Magazin', 'App']

start = datetime(2024, 1, 1)
df = pd.DataFrame({
    'order_id': range(1, n + 1),
    'customer_id': np.random.randint(1, 5000, n),
    'order_date': [
        start + timedelta(days=int(d), hours=int(h))
        for d, h in zip(
            np.random.randint(0, 700, n),
            np.random.randint(0, 24, n),
        )
    ],
    'oras': np.random.choice(
        orase, n, p=[0.35, 0.15, 0.10, 0.12, 0.10, 0.10, 0.08]
    ),
    'categorie': np.random.choice(categorii, n),
    'canal': np.random.choice(canal, n, p=[0.55, 0.35, 0.10]),
    'amount_ron': np.random.lognormal(4.5, 1.0, n).round(2),
    'discount_pct': np.random.choice(
        [0, 5, 10, 15, 20, 30], n,
        p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02],
    ),
    'rating': np.random.choice(
        [1, 2, 3, 4, 5, np.nan], n,
        p=[0.05, 0.05, 0.10, 0.30, 0.40, 0.10],
    ),
})

# Adaugă null-uri intenționat (ca în viața reală)
df.loc[df.sample(frac=0.05).index, 'oras'] = np.nan
df.loc[df.sample(frac=0.03).index, 'amount_ron'] = np.nan

# Salvează în folder data/
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
df.to_parquet(data_dir / 'vanzari_ro.parquet')

print(f"✅ Salvat {len(df):,} rânduri în data/vanzari_ro.parquet")
print(f"📊 Coloane: {list(df.columns)}")
print(f"📅 Perioada: {df.order_date.min()} → {df.order_date.max()}")