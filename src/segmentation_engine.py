# Demographic, tenure, credit, and high-value customer binning logic
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def apply_customer_segmentation(df: pd.DataFrame) -> pd.DataFrame:
    """Generates all derived analytical dimensions according to ECB project methodology."""
    df_seg = df.copy()
    
    # 1. Age Segmentation (<30, 30-45, 46-60, 60+)
    age_bins = [0, 29, 45, 60, 120]
    age_labels = ['<30', '30–45', '46–60', '60+']
    df_seg['Age_Group'] = pd.cut(df_seg['Age'], bins=age_bins, labels=age_labels, right=True)
    
    # 2. Credit Score Tiers (Low: <580, Medium: 580-670, High: >670)
    credit_bins = [0, 579, 670, 900]
    credit_labels = ['Low (<580)', 'Medium (580–670)', 'High (>670)']
    df_seg['Credit_Tier'] = pd.cut(df_seg['CreditScore'], bins=credit_bins, labels=credit_labels, right=True)
    
    # 3. Tenure Cohorts (New: 0-2, Mid-term: 3-7, Long-term: 8-10)
    tenure_bins = [-1, 2, 7, 15]
    tenure_labels = ['New (0–2 yrs)', 'Mid-term (3–7 yrs)', 'Long-term (8–10 yrs)']
    df_seg['Tenure_Group'] = pd.cut(df_seg['Tenure'], bins=tenure_bins, labels=tenure_labels, right=True)
    
    # 4. Balance Classification (Zero-Balance, Low-Balance: <=50k, High-Balance: >50k)
    def classify_balance(bal: float) -> str:
        if bal == 0:
            return 'Zero-Balance'
        elif bal <= 50000:
            return 'Low-Balance (<=€50K)'
        else:
            return 'High-Balance (>€50K)'
            
    df_seg['Balance_Segment'] = df_seg['Balance'].apply(classify_balance)
    
    # 5. Financial Risk Flags & Ratios
    df_seg['Balance_to_Salary_Ratio'] = np.where(df_seg['EstimatedSalary'] > 0, df_seg['Balance'] / df_seg['EstimatedSalary'], 0.0)
    df_seg['Activity_Status'] = df_seg['IsActiveMember'].apply(lambda x: 'Active Member' if x == 1 else 'Inactive Member')
    df_seg['Credit_Card_Status'] = df_seg['HasCrCard'].apply(lambda x: 'Has Credit Card' if x == 1 else 'No Credit Card')
    df_seg['Churn_Status'] = df_seg['Exited'].apply(lambda x: 'Churned (Exited)' if x == 1 else 'Retained (Active)')
    
    return df_seg