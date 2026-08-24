import numpy as np
import pandas as pd

np.random.seed(42)

states = ["IL", "CA", "TX", "NY", "OH", "GA", "MI", "PA", "NC", "AZ"]
conditions = ["Diabetes", "Obesity", "Coronary Heart Disease", "Asthma", "High Blood Pressure", "Depression"]
n_counties_per_state = 15


def make_county_list():
    rows = []
    fips_counter = 1
    for state in states:
        for i in range(n_counties_per_state):
            rows.append({
                "state": state,
                "county_fips": f"{states.index(state)+1:02d}{fips_counter:03d}",
                "county_name": f"{state} County {i+1}",
            })
            fips_counter += 1
    return pd.DataFrame(rows)


def make_places_sample(counties: pd.DataFrame) -> pd.DataFrame:
    df = counties.copy()
    base_rates = {"Diabetes": 11, "Obesity": 33, "Coronary Heart Disease": 6.5,
                  "Asthma": 9.5, "High Blood Pressure": 32, "Depression": 20}
    for cond in conditions:
        base = base_rates[cond]
        df[f"{cond}_pct"] = np.clip(
            np.random.normal(loc=base, scale=base * 0.25, size=len(df)), 1, 60
        ).round(1)
    df["total_population"] = np.random.randint(8_000, 950_000, size=len(df))
    return df


def make_hrsa_sample(counties: pd.DataFrame) -> pd.DataFrame:
    df = counties[["county_fips", "state", "county_name"]].copy()
    df["hpsa_score"] = np.random.randint(0, 26, size=len(df))
    df["designation_type"] = np.where(
        df["hpsa_score"] >= 14, "High Need", np.where(df["hpsa_score"] >= 7, "Moderate Need", "Low Need")
    )
    return df


if __name__ == "__main__":
    counties = make_county_list()
    places = make_places_sample(counties)
    hrsa = make_hrsa_sample(counties)

    places.to_csv("places_sample.csv", index=False)
    hrsa.to_csv("hrsa_sample.csv", index=False)

    print(f"Wrote places_sample.csv ({len(places)} rows)")
    print(f"Wrote hrsa_sample.csv ({len(hrsa)} rows)")
