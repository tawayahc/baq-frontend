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

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = self._url(path)
        try:
            resp = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=self.timeout
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def predict(self, forecast_horizon: int) -> Dict[str, Any]:
        return self._post("/predict/next", {"forecast_horizon": forecast_horizon})

    def single_step(self) -> Dict[str, Any]:
        return self.predict(1)

    def multi_step(self, steps: int = 48) -> Dict[str, Any]:
        return self.predict(steps)
