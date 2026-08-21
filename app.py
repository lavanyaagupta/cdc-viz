import sys
import pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from data.data_pipeline import build_merged_dataset

st.set_page_config(page_title="Healthcare Access vs. Disease Burden", layout="wide")
st.title("Healthcare Access vs. Chronic Disease Burden")
st.caption("Which counties carry the highest chronic disease burden relative to the ir"
           "access to primary care? Built on CDC PLACES + HRSA HPSA data.")

@st.cache_data
def load_data():
  return build_merged_data()

df = load_data()

st.sidebar.header("Filters")
states = st.sidebar.multiselect(
  "State", options=sorted(df["state"].unique()), default=sorted(df["state"].unique()))
min_gap, max_gap = st.sidebar.slider(
  "Gap score range", float(df["gap_score"].min()), float(df["gap_score"].max()),
  (float(df["gap_score"].min()), float(df["gap_score"].max())),)

filtered = df[
  df["state"].isin(states)
  & df["gap_score"].between(min_gap, max_gap)
]
