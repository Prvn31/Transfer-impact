import streamlit as st
import pandas as pd

st.title("Summer 2026's biggest attacking signings: worth the money?")
st.caption("Data: FotMob (Opta), league games only, as of 23 Oct 2026")

import matplotlib.pyplot as plt

df = pd.read_csv('transfers.csv')

# Expected goal contributions per 90, this season and last
df['xgc_per_90'] = (df['xg'] + df['xa']) / df['minutes'] * 90
df['prev_xgc_per_90'] = (df['prev_xg'] + df['prev_xa']) / df['prev_minutes'] * 90

# Value for money: fee per unit of output (lower = better value)
df['cost_per_xgc90'] = df['fee_m'] / df['xgc_per_90']

# Change since last season, as a percentage
df['xgc_change_pct'] = (df['xgc_per_90'] - df['prev_xgc_per_90']) / df['prev_xgc_per_90'] * 100

# Verdict: above group average = natural fit; small drop = steady; big drop = still adjusting
avg = df['xgc_per_90'].mean()

def fit_verdict(xgc, change):
    if xgc >= avg:
        return '🟢 Natural fit'
    elif change >= -10:
        return '🟡 Steady'
    else:
        return '🔴 Still adjusting'

verdicts = []
for xgc, change in zip(df['xgc_per_90'], df['xgc_change_pct']):
    verdicts.append(fit_verdict(xgc, change))
df['verdict'] = verdicts

# Ranked copy: best output first, numbered from 1 (df itself stays unsorted)
by_output = df.sort_values('xgc_per_90', ascending=False).reset_index(drop=True)
by_output.index = by_output.index + 1

by_output[['name', 'fee_m', 'xgc_per_90', 'cost_per_xgc90', 'xgc_change_pct', 'verdict']].round(2)

table = by_output[['name', 'fee_m', 'xgc_per_90', 'cost_per_xgc90', 'xgc_change_pct', 'verdict']].rename(columns={
    'name': 'Player',
    'fee_m': '_____',
    'xgc_per_90': '_____',
    'cost_per_xgc90': '_____',
    'xgc_change_pct': '_____',
    'verdict': 'Verdict'
})

st.dataframe(table.round(2))
