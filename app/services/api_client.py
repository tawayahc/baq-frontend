import requests
import streamlit as st
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self,
                 base_url: Optional[str] = None,
                 token: Optional[str] = None,
                 timeout: int = 10):
        self.base_url = base_url or st.secrets["API_BASE_URL"].rstrip("/")
        self.token = token or st.secrets.get("API_TOKEN", "")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        hdrs = {"Content-Type": "application/json"}
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
        return hdrs

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._url(path)
        try:
            resp = requests.get(url,
                                headers=self._headers(),
                                params=params,
                                timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def single_step(self):
        return {
            "predictions": [13.59821891784668]
        }
    
    def multi_step(self):
        return {
            "predictions": [
                { "predicted_value": 13.598218762874602 },
                { "predicted_value": 13.670179290324448 },
                { "predicted_value": 13.598976705968377 },
                { "predicted_value": 13.53243488408625 },
                { "predicted_value": 13.499098607897757 },
                { "predicted_value": 13.479907665029167 },
                { "predicted_value": 13.46512483693659 },
                { "predicted_value": 13.453978960588573 },
                { "predicted_value": 13.445807570219038 },
                { "predicted_value": 13.439636797085402 },
                { "predicted_value": 13.43477186001837 },
                { "predicted_value": 13.430920451506971 },
                { "predicted_value": 13.427888679131863 },
                { "predicted_value": 13.425526716932653 },
                { "predicted_value": 13.42383897155523 },
                { "predicted_value": 13.422558106482027 },
                { "predicted_value": 13.42147700935602 },
                { "predicted_value": 13.420603024587033 },
                { "predicted_value": 13.41989943012595 },
                { "predicted_value": 13.419364757090806 },
                { "predicted_value": 13.419079793989656 },
                { "predicted_value": 13.418869743868706 },
                { "predicted_value": 13.418868274986743 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 },
                { "predicted_value": 13.418809519708155 }
            ]
        }