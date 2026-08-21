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

# top line metrics
col1, col2, col3 = st.columns(3)
col1.metric("Counties shown", len(filtered))
col2.metric("Avg. disease burden index", f"{filtered['disease_burden_index'].mean():.1f}%")
col3.metric("Avg. HPSA  shortage score", f"{filtered['hpsa_score'].mean():.1f}")
st.divider()

# scatter: burden vs. access
st.subheader("Burden vs. Access, by County")
fig_scatter = px.scatter( filtered, x="access_percentile", y="burden_percentile", color="gap_score", color_continuous_scale="RdY1Bu_r", hover_data=["county_name", "state", "disease_buden_index", "hpsa_score"],
                         labels = {
                                    "access_percentile": "Access Percentile (higher = better access)",
                                    "burden_percentile": "Disease Burden Percentile (higher = worse)",
                                    "gap_score": "Gap Score",
                         },
                        )
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter,use_container_width=True)
st.caption("Top-left quadrant = highest priority: highest disease burden, low healthcare access.")

st.subheader("Most underserved Counties (highest gap score)")
top_n = st.slider("Show top N counties", 5,30,10)
st.dataframe(filtered.nlargest(top_n, "gap_score")[
             ["county_name", "state", "disease_burden_index", "hpsa_score", "designation_type", "gap_score"]
             ].round(1),
             use_container_width=True,
             hide_index=True,)

st.subheader("Average Gap Score by State")
state_avg = filtered.groupby("state")["gap_score"].mean().sort_values(ascending=False).resert_index()
fig_bar = px.bar(state_avg, x="state", y="gap_score", color="gap_scpre", color_continuous_scale = "RdY1Bu_r")
fig_bar.update_layout(height=400)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption("Data: CDC Places + HRSA HPSA (primary care shortage areas). "
           "Sample data shown until real CSVs")
