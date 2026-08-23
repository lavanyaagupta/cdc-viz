"""
app.py — Healthcare Access vs. Chronic Disease Burden Dashboard
Run locally: streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from data_pipeline import build_merged_dataset

st.set_page_config(page_title="Healthcare Access vs. Disease Burden", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    div[data-testid="stMetric"] {
        background-color: #F4F1EA;
        border-radius: 10px;
        padding: 14px 16px;
        border: 1px solid #E9E5DA;
            }
    div[data-testid="stMetricLabel"] { font-weight: 500; }
    .insight-box {
        background-color: #FFF3EC;
        border-left: 4px solid #E76F51;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Healthcare Access vs. Chronic Disease Burden")
st.caption(
    "Which counties carry the highest chronic disease burden relative to their "
    "access to primary care? Built on CDC PLACES + HRSA HPSA data."
)


@st.cache_data
def load_data():
    return build_merged_dataset()


df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect(
    "State", options=sorted(df["state"].unique()), default=sorted(df["state"].unique())
)
min_gap, max_gap = st.sidebar.slider(
    "Gap score range", float(df["gap_score"].min()), float(df["gap_score"].max()),
    (float(df["gap_score"].min()), float(df["gap_score"].max())),
)

filtered = df[
    df["state"].isin(states)
    & df["gap_score"].between(min_gap, max_gap)
]

# Top-line metrics
col1, col2, col3 = st.columns(3)
col1.metric("Counties shown", len(filtered))
col2.metric("Avg. disease burden index", f"{filtered['disease_burden_index'].mean():.1f}%")
col3.metric("Avg. HPSA shortage score", f"{filtered['hpsa_score'].mean():.1f}")

st.divider()

# generate insights
top_county = filtered.iloc[0]
top_state = filtered.groupby("state")["gap_score"].mean().idmax()
top_state_avg = filtered.groupby("state")["gap_score"].mean().max()

st.markdown(
    f"""
    <div class="insight-box">
    <b>{top_county['county_name']}, {top_county['state']}</b> has the highest burden-access gap 
    in the current view — disease burden in the {top_county['burden_percentile']:.0f}th percentile
    paired with an HPSA shortage score of {top_county['hpsa_score']:.0f}.
    <br><b>{top_state}</b> has the highest average gap score among filtered states
    ({top_state_avg:.1f}), suggesting it as a priority region for expanding access.
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider

# Scatter: burden vs. access
st.subheader("Burden vs. Access, by County")
fig_scatter = px.scatter(
    filtered,
    x="access_percentile",
    y="burden_percentile",
    color="gap_score",
    color_continuous_scale="RdYlBu_r",
    hover_data=["county_name", "state", "disease_burden_index", "hpsa_score"],
    labels={
        "access_percentile": "Access Percentile (higher = better access)",
        "burden_percentile": "Disease Burden Percentile (higher = worse)",
        "gap_score": "Gap Score",
    },
)
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption("Top-left quadrant = highest priority: high disease burden, low healthcare access.")

# Top underserved counties table
st.subheader("Most Underserved Counties (highest gap score)")
top_n = st.slider("Show top N counties", 5, 30, 10)
st.dataframe(
    filtered.nlargest(top_n, "gap_score")[
        ["county_name", "state", "disease_burden_index", "hpsa_score", "designation_type", "gap_score"]
    ].round(1),
    use_container_width=True,
    hide_index=True,
)

# Bar chart by state
st.subheader("Average Gap Score by State")
state_avg = filtered.groupby("state")["gap_score"].mean().sort_values(ascending=False).reset_index()
fig_bar = px.bar(state_avg, x="state", y="gap_score", color="gap_score", color_continuous_scale="RdYlBu_r")
fig_bar.update_layout(height=400)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.caption(
    "Data: CDC PLACES (chronic disease prevalence) + HRSA HPSA (primary care shortage areas)."
)
