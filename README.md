# 🌤️ BAQ Frontend – Bangkok Air Quality Dashboard

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

**Live app →** [https://baq-frontend.streamlit.app/](https://baq-frontend.streamlit.app/)



## 📌 Overview

BAQ Frontend is a web-based dashboard built with Streamlit to visualize and forecast air quality and weather conditions in **Bangkok**.

Key functionalities include:

- 🔮 PM2.5 prediction (1-step and multi-step up to 48 hours)
- 📊 Trend, distribution, and correlation visualizations
- 🕒 Time-based heatmaps and insights
- 🧾 Historical data browsing from S3 or API
- ☁️ Hosted via Streamlit Cloud


## 🗂 Project Structure
```
BAQ-FRONTEND/
├── .streamlit/
│   └── secrets.toml       # 🔒 API keys & credentials (not pushed to GitHub)
├── app/
│   ├── components/
│   │   └── sidebar.py     # Sidebar layout
│   ├── services/
│   │   ├── api_client.py  # REST API client for predictions
│   │   └── data_loader.py # S3 data loader
│   ├── utils/
│   │   ├── dashboard.py   # All dashboard visualizations
│   │   └── plot.py        # Common plotting utilities
│   └── main.py            # 🚀 Streamlit app entry point
├── .gitignore
├── requirements.txt
└── README.md
```


## ⚙️ Installation (Local Development)

1. Clone the repository:
```bash
git clone https://github.com/your-username/baq-frontend.git
cd baq-frontend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


## 🔐 Configuration

Create .streamlit/secrets.toml (do NOT push this file):
```
AWS_S3_BUCKET         = "your-bucket"
AWS_ACCESS_KEY_ID     = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret"
AWS_REGION            = "ap-southeast-1"

API_BASE_URL = "http://your-api-url"
API_TOKEN    = "optional-token"
```
> On Streamlit Cloud, go to App → Settings → Secrets and paste your credentials there.

## 🚀 Run the App
```bash
streamlit run app/main.py
```
> Then open [http://localhost:8501](http://localhost:8501) in your browser.


## 📤 Deploy to Streamlit Cloud
1. Push your code to GitHub (excluding .env and secrets.toml)
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and configure Secrets in the UI
4. Done 🎉
