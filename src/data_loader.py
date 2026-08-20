# Ingestion, validation, cleaning, and categorical binning
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_raw_banking_data(file_path: str = "data/raw/European_Bank.csv") -> pd.DataFrame:
    """Loads and validates the European banking transaction dataset."""
    df = pd.read_csv(file_path)
    
    # Validation & Cleaning
    df = df.dropna(subset=['CustomerId', 'CreditScore', 'Geography', 'Gender', 'Age', 'Balance', 'Exited'])
    df['CustomerId'] = df['CustomerId'].astype(str)
    df['CreditScore'] = pd.to_numeric(df['CreditScore'], errors='coerce')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Tenure'] = pd.to_numeric(df['Tenure'], errors='coerce')
    df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
    df['EstimatedSalary'] = pd.to_numeric(df['EstimatedSalary'], errors='coerce')
    df['Exited'] = pd.to_numeric(df['Exited'], errors='coerce').astype(int)
    
    return df