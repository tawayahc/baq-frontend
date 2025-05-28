import boto3
import pandas as pd
import streamlit as st
from io import StringIO
from botocore.exceptions import ClientError

class S3DataLoader:
    """
    OOP wrapper for loading and cleaning CSV data from S3,
    with credentials & config pulled from a .env file.
    """

    def __init__(self):
        # Read config from environment
        self.bucket = st.secrets["AWS_S3_BUCKET"]
        aws_key = st.secrets["AWS_ACCESS_KEY_ID"]
        aws_secret = st.secrets["AWS_SECRET_ACCESS_KEY"]
        aws_region = st.secrets["AWS_REGION"]

        if not self.bucket or not aws_key or not aws_secret:
            raise ValueError(
                "Missing one of AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY in environment"
            )

        # Initialize boto3 session & client
        session = boto3.Session(
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )
        self.s3 = session.client("s3")

    def load_csv(self, key: str, encoding: str = "utf-8") -> pd.DataFrame:
        """
        Download a CSV from S3 and return as DataFrame.
        """
        try:
            resp = self.s3.get_object(Bucket=self.bucket, Key=key)
            body = resp["Body"].read().decode(encoding)
            return pd.read_csv(StringIO(body))
        except ClientError as e:
            print(f"[Error] Failed to fetch {key} from {self.bucket}: {e}")
            return pd.DataFrame()

    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DataFrame columns and drop unwanted fields.
        """
        if data is None or data.empty:
            print("[Warning] No data to clean.")
            return pd.DataFrame()

        # Normalize column names
        data.columns = (
            data.columns
                .str.replace(r'\s*\(\)', '', regex=True)
                .str.replace(' ', '_', regex=False)
        )

        # Parse time column
        if 'time' in data.columns:
            data['time'] = pd.to_datetime(data['time'], errors='coerce')

        # Drop extra columns
        to_drop = [
            "carbon_dioxide_(ppm)",
            "methane_(μg/m³)",
            "snowfall_(cm)",
            "snow_depth_(m)"
        ]
        data = data.drop(columns=[c for c in to_drop if c in data.columns], errors='ignore')
        return data

    def get_data(self, key: str) -> pd.DataFrame:
        df = self.load_csv(key)
        return self._clean_data(df)
