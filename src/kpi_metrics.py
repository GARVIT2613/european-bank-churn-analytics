# Calculation of churn rates, capital at risk, GRI, and odds ratios
import pandas as pd
import numpy as np
from typing import Dict

def compute_executive_banking_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """Calculates enterprise portfolio KPIs and capital-at-risk exposure."""
    total_customers = len(df)
    total_capital = float(df['Balance'].sum())
    churned_customers = int(df['Exited'].sum())
    retained_customers = total_customers - churned_customers
    
    churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0.0
    
    churned_balance = float(df.loc[df['Exited'] == 1, 'Balance'].sum())
    capital_at_risk_pct = (churned_balance / total_capital * 100) if total_capital > 0 else 0.0
    
    active_members = int(df['IsActiveMember'].sum())
    active_ratio = (active_members / total_customers * 100) if total_customers > 0 else 0.0
    
    # High-Value Churn Ratio (Top 25% Balance Quartile)
    p75_balance = df['Balance'].quantile(0.75)
    hv_df = df[df['Balance'] >= p75_balance]
    hv_churn_rate = (hv_df['Exited'].mean() * 100) if len(hv_df) > 0 else 0.0
    
    # Inactive vs Active Churn Spread
    inactive_churn = (df[df['IsActiveMember'] == 0]['Exited'].mean() * 100) if len(df[df['IsActiveMember'] == 0]) > 0 else 0.0
    active_churn = (df[df['IsActiveMember'] == 1]['Exited'].mean() * 100) if len(df[df['IsActiveMember'] == 1]) > 0 else 0.0
    activity_drag_differential = inactive_churn - active_churn
    
    return {
        "total_customers": total_customers,
        "total_capital": total_capital,
        "churned_customers": churned_customers,
        "retained_customers": retained_customers,
        "churn_rate": churn_rate,
        "churned_balance": churned_balance,
        "capital_at_risk_pct": capital_at_risk_pct,
        "active_ratio": active_ratio,
        "hv_churn_rate": hv_churn_rate,
        "activity_drag_differential": activity_drag_differential
    }

def calculate_geographic_risk_index(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the Geographic Risk Index (GRI) normalized against baseline portfolio churn."""
    baseline_churn = df['Exited'].mean()
    geo = df.groupby('Geography').agg(
        Total_Accounts=('CustomerId', 'count'),
        Churned_Accounts=('Exited', 'sum'),
        Total_Balance=('Balance', 'sum'),
        Churned_Balance=('Balance', lambda x: df.loc[x.index[df.loc[x.index, 'Exited'] == 1], 'Balance'].sum())
    ).reset_index()
    
    geo['Churn_Rate'] = (geo['Churned_Accounts'] / geo['Total_Accounts']) * 100
    geo['GRI'] = (geo['Churn_Rate'] / (baseline_churn * 100)) if baseline_churn > 0 else 1.0
    geo['Capital_Loss_Share'] = (geo['Churned_Balance'] / geo['Churned_Balance'].sum()) * 100
    return geo