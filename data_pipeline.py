"""
Loads CDC places and HRSA HPSA, merges them at county level, and computes a burden access gap shortage
gap_score = disease_burden_percentile - health_access_percentile
high gap score means that disease burden is high and access is poor realtive to other counties -> these are the counties most underserved relative to their need
"""
import pandas as pd

# file location
places_path = r"C:\Users\lavan\Downloads\places_sample.csv"
hrsa_path = r"C:\Users\lavan\Downloads\hrsa_sample.csv"
use_sample_schema = True #set false when using real places/hrsa column names

conditions_columns_sample = ["Diabetes_pct", "Obestity_pct", "Coronary Heart Disease_pct", "Asthma_pct", "High Blood Pressure_pct", "Depression_pct"]
condition_columns_real = ["DIABETES_CrudePrev", "OBESITY_CrudePrev", "CHD_CrudePrev", "CASTHMA_CrudePrev", "BPHIGH_CrudePrev", "DEPRESSION_CrudePrev"]

# load places
def load_hrsa(path: str = hrsa_path) -> pd.DataFrame:
  df = pd.read_csv(path, dtype={"county_fips", str})
  return df[["county_fips", "hpsa_score", "designation_type"]]

def build_merged_dataset() -> pd.DataFrame:
  places = load_place()
  hrsa = load_hrsa()
  merged = places.merge(hrsa, on="county_fips", how="inner")

  merged["burden_percentile"] = merged["disease_burden_index"].rank(pct=True) *100
  merged["access_percentile"] = 100 - (merged["hpsa_score"].rank(pct=True) * 100)
  merged["gap_score"] = merged["burden_percentile"] - merged["access_percentile"]
  return merged.sort_values("gap_score", ascending=False).reset_index(drop=True)

if __name__ = "__main__":
  df = build_merged_dataset()
  df.to_csv("data/merged_county_data.csv", index=False)
  print(df[["county_name", "state", "disease_burden_index", "hpsa_score", "gap_score"]].head())

  # merged dataset 
