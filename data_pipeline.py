"""
Loads CDC PLACES and HRSA HPSA data, merges at the county level, and computes
a burden-access gap score:

gap_score = disease_burden_percentile - healthcare_access_percentile

A high gap score means disease burden is high AND access is poor relative to
other counties -> these are the counties most underserved relative to need.
"""
import pandas as pd

PLACES_PATH = "places_sample.csv"
HRSA_PATH = "hrsa_sample.csv"

CONDITION_COLUMNS_SAMPLE = [
    "Diabetes_pct", "Obesity_pct", "Coronary Heart Disease_pct",
    "Asthma_pct", "High Blood Pressure_pct", "Depression_pct",
]


def load_places(path: str = PLACES_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"county_fips": str})
    df["disease_burden_index"] = df[CONDITION_COLUMNS_SAMPLE].mean(axis=1)
    return df


def load_hrsa(path: str = HRSA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"county_fips": str})
    return df[["county_fips", "hpsa_score", "designation_type"]]


def build_merged_dataset() -> pd.DataFrame:
    places = load_places()
    hrsa = load_hrsa()

    merged = places.merge(hrsa, on="county_fips", how="inner")

    merged["burden_percentile"] = merged["disease_burden_index"].rank(pct=True) * 100
    merged["access_percentile"] = 100 - (merged["hpsa_score"].rank(pct=True) * 100)
    merged["gap_score"] = merged["burden_percentile"] - merged["access_percentile"]

    return merged.sort_values("gap_score", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    df = build_merged_dataset()
    df.to_csv("merged_county_data.csv", index=False)
    print(df[["county_name", "state", "disease_burden_index", "hpsa_score", "gap_score"]].head())
