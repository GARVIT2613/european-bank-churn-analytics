# What-If retention scenario modeling and capital recovery engine
import pandas as pd
import numpy as np
from typing import Tuple, Dict

def run_retention_simulation(
    df: pd.DataFrame,
    german_retention_boost: float,
    midage_retention_boost: float,
    cross_sell_migration_pct: float
) -> Dict[str, float]:
    """
    Simulates capital preservation and portfolio churn reduction under targeted policies.
    - german_retention_boost: % reduction in German customer churn
    - midage_retention_boost: % reduction in 46-60 customer churn
    - cross_sell_migration_pct: % of 1-product users converted to 2-product users
    """
    sim_df = df.copy()
    base_churned_bal = sim_df.loc[sim_df['Exited'] == 1, 'Balance'].sum()
    base_churn_count = sim_df['Exited'].sum()
    
    # 1. German Intervention Savings
    german_churners = sim_df[(sim_df['Geography'] == 'Germany') & (sim_df['Exited'] == 1)]
    german_saved_bal = german_churners['Balance'].sum() * (german_retention_boost / 100.0)
    german_saved_count = len(german_churners) * (german_retention_boost / 100.0)
    
    # 2. Middle-Age Intervention Savings
    midage_churners = sim_df[(sim_df['Age_Group'] == '46–60') & (sim_df['Exited'] == 1)]
    midage_saved_bal = midage_churners['Balance'].sum() * (midage_retention_boost / 100.0)
    midage_saved_count = len(midage_churners) * (midage_retention_boost / 100.0)
    
    # 3. Product Cross-Selling Migration Savings (1 Prod churn 27.7% -> 2 Prod churn 7.58%)
    single_prod_churners = sim_df[(sim_df['NumOfProducts'] == 1) & (sim_df['Exited'] == 1)]
    cross_sell_saved_count = len(single_prod_churners) * (cross_sell_migration_pct / 100.0) * (1 - (7.58 / 27.71))
    cross_sell_saved_bal = single_prod_churners['Balance'].sum() * (cross_sell_migration_pct / 100.0) * (1 - (7.58 / 27.71))
    
    total_preserved_capital = german_saved_bal + midage_saved_bal + cross_sell_saved_bal
    total_saved_customers = german_saved_count + midage_saved_count + cross_sell_saved_count
    
    sim_final_loss = max(0.0, base_churned_bal - total_preserved_capital)
    sim_final_churned_count = max(0.0, base_churn_count - total_saved_customers)
    sim_churn_rate = (sim_final_churned_count / len(sim_df)) * 100.0
    
    return {
        "base_capital_loss": base_churned_bal,
        "total_preserved_capital": total_preserved_capital,
        "sim_final_loss": sim_final_loss,
        "german_saved_bal": german_saved_bal,
        "midage_saved_bal": midage_saved_bal,
        "cross_sell_saved_bal": cross_sell_saved_bal,
        "sim_churn_rate": sim_churn_rate,
        "churn_rate_reduction": (base_churn_count / len(sim_df) * 100.0) - sim_churn_rate
    }