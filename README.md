# cdc-viz

This project is county-level dashboard that identifies where chronic disease burden is highest relative to primary care access.

# The Question
While the presentation of raw prevalence in most public health dashboards, what we really need to address here is where is need the highest and where is access the lowest at the same time? A county with a high disease burden but good provider coverage is a very different problem than a country with the same burden and no providers. To address the question at hand, this project combines two federal datasets: CDC PLACES and HRSA Health Professional Shortage Areas. I am computing a Burden-Access Gap Score, which is each county's disease burden percentile minus its healthcare access percentile. I expect that counties with the highest gap scores are the ones carrying the most disease burden with the least capacity to treat it.

# Tech Stack
- Python/pandas for data cleaning, merging, percentile-based scoring
- Plotly for interactive bar charts and scatter plots
- Streamlit for the dashboard framework, using the Streamlit Community Cloud

# Project Structure
health-access-dashboard/
├── data/
│   ├── generate_sample_data.py   # synthetic data matching real schema (for testing)
│   ├── data_pipeline.py          # load, merge, compute gap score
│   ├── places_sample.csv         # sample data (swap for real PLACES export)
│   └── hrsa_sample.csv           # sample data (swap for real HRSA export)
├── app/
│   └── app.py                    # Streamlit dashboard
├── requirements.txt
└── README.md

# To Run Locally
pip install -r requirements.txt
python data/generate_sample_data.py
streamlit run app/app.py

# Requirements
streamlit>=1.35
pandas>=2.0
plotly>=5.20
numpy>=1.26
