# Plotly charts (2x2 grid per module), sunbursts, and heatmaps
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# TAB 1: EXECUTIVE PORTFOLIO OVERVIEW (4 Visuals)
# ---------------------------------------------------------
def build_capital_flow_bar(df: pd.DataFrame) -> go.Figure:
    geo_bal = df.groupby(['Geography', 'Churn_Status'])['Balance'].sum().reset_index()
    fig = px.bar(
        geo_bal,
        x='Geography',
        y='Balance',
        color='Churn_Status',
        barmode='stack',
        color_discrete_map={'Retained (Active)': '#2563EB', 'Churned (Exited)': '#EF4444'},
        template='plotly_white'
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Deposit Capital (€)", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_portfolio_sunburst(df: pd.DataFrame) -> go.Figure:
    fig = px.sunburst(
        df,
        path=['Geography', 'Gender', 'Churn_Status'],
        values='Balance',
        color='Churn_Status',
        color_discrete_map={'Retained (Active)': '#3B82F6', 'Churned (Exited)': '#EF4444', '(?)': '#CBD5E1'},
        template='plotly_white'
    )
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    return fig

def build_tenure_churn_curve(df: pd.DataFrame) -> go.Figure:
    tenure_df = df.groupby('Tenure').agg(
        Total=('CustomerId', 'count'),
        Churn_Rate=('Exited', lambda x: x.mean() * 100)
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tenure_df['Tenure'], y=tenure_df['Total'], name='Customer Volume', marker_color='#CBD5E1', yaxis='y1'))
    fig.add_trace(go.Scatter(x=tenure_df['Tenure'], y=tenure_df['Churn_Rate'], name='Churn Rate (%)', line=dict(color='#EF4444', width=3), mode='lines+markers', yaxis='y2'))
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Customer Count", showgrid=True, gridcolor="#F1F5F9"),
        yaxis2=dict(title="Churn Rate (%)", overlaying="y", side="right", range=[0, 40], showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_credit_score_box(df: pd.DataFrame) -> go.Figure:
    fig = px.box(
        df,
        x='Churn_Status',
        y='CreditScore',
        color='Churn_Status',
        color_discrete_map={'Retained (Active)': '#2563EB', 'Churned (Exited)': '#EF4444'},
        template='plotly_white'
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    return fig

# ---------------------------------------------------------
# TAB 2: GEOGRAPHIC & REGIONAL EXPOSURE (4 Visuals)
# ---------------------------------------------------------
def build_cross_border_churn_bar(df: pd.DataFrame) -> go.Figure:
    geo_churn = df.groupby('Geography')['Exited'].mean().reset_index()
    geo_churn['Churn_Rate'] = geo_churn['Exited'] * 100
    geo_churn = geo_churn.sort_values('Churn_Rate', ascending=True)
    
    fig = px.bar(
        geo_churn,
        x='Churn_Rate',
        y='Geography',
        orientation='h',
        color='Churn_Rate',
        color_continuous_scale='Reds',
        template='plotly_white',
        text=geo_churn['Churn_Rate'].apply(lambda x: f"{x:.2f}%")
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), coloraxis_showscale=False)
    return fig

def build_regional_capital_loss_donut(df: pd.DataFrame) -> go.Figure:
    churned_geo = df[df['Exited'] == 1].groupby('Geography')['Balance'].sum().reset_index()
    fig = go.Figure(data=[go.Pie(
        labels=churned_geo['Geography'],
        values=churned_geo['Balance'],
        hole=.55,
        marker_colors=['#3B82F6', '#EF4444', '#F59E0B']
    )])
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=10))
    return fig

def build_geo_activity_matrix(df: pd.DataFrame) -> go.Figure:
    geo_act = df.groupby(['Geography', 'Activity_Status'])['Exited'].mean().reset_index()
    geo_act['Churn_Rate'] = geo_act['Exited'] * 100
    
    fig = px.bar(
        geo_act,
        x='Geography',
        y='Churn_Rate',
        color='Activity_Status',
        barmode='group',
        color_discrete_map={'Active Member': '#10B981', 'Inactive Member': '#EF4444'},
        template='plotly_white'
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Churn Rate (%)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_balance_salary_geo_scatter(df: pd.DataFrame) -> go.Figure:
    sample_df = df.sample(min(1200, len(df)), random_state=42)
    fig = px.scatter(
        sample_df,
        x='EstimatedSalary',
        y='Balance',
        color='Geography',
        symbol='Churn_Status',
        color_discrete_sequence=['#2563EB', '#EF4444', '#F59E0B'],
        opacity=0.7,
        template='plotly_white'
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig

# ---------------------------------------------------------
# TAB 3: DEMOGRAPHIC & JOURNEY ANALYTICS (4 Visuals)
# ---------------------------------------------------------
def build_age_risk_dual_axis(df: pd.DataFrame) -> go.Figure:
    age_data = df.groupby('Age_Group', observed=False).agg(
        Total=('CustomerId', 'count'),
        Churn_Rate=('Exited', lambda x: x.mean() * 100)
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=age_data['Age_Group'], y=age_data['Total'], name='Customer Count', marker_color='#CBD5E1', yaxis='y1'))
    fig.add_trace(go.Scatter(x=age_data['Age_Group'], y=age_data['Churn_Rate'], name='Churn Rate (%)', line=dict(color='#DC2626', width=3), mode='lines+markers', yaxis='y2'))
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Account Base"),
        yaxis2=dict(title="Churn Rate (%)", overlaying="y", side="right", range=[0, 70], showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_product_saturation_bar(df: pd.DataFrame) -> go.Figure:
    prod_churn = df.groupby('NumOfProducts').agg(
        Count=('CustomerId', 'count'),
        Churn_Rate=('Exited', lambda x: x.mean() * 100)
    ).reset_index()
    
    fig = px.bar(
        prod_churn,
        x='NumOfProducts',
        y='Churn_Rate',
        color='Churn_Rate',
        color_continuous_scale='Reds',
        text=prod_churn['Churn_Rate'].apply(lambda x: f"{x:.1f}%"),
        template='plotly_white'
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="Number of Bank Products Held", tickvals=[1, 2, 3, 4]),
        yaxis=dict(title="Churn Rate (%)", range=[0, 110]),
        coloraxis_showscale=False
    )
    return fig

def build_gender_disparity_waterfall(df: pd.DataFrame) -> go.Figure:
    baseline = df['Exited'].mean() * 100
    female_churn = df[df['Gender'] == 'Female']['Exited'].mean() * 100
    male_churn = df[df['Gender'] == 'Male']['Exited'].mean() * 100
    
    fig = go.Figure(go.Waterfall(
        name="Gender Variance",
        orientation="v",
        x=["Portfolio Baseline", "Female Premium Drag", "Male Retention Advantage", "Final Active Rate"],
        y=[baseline, female_churn - baseline, male_churn - baseline, 0],
        measure=["relative", "relative", "relative", "total"],
        decreasing={"marker": {"color": "#10B981"}},
        increasing={"marker": {"color": "#EF4444"}},
        totals={"marker": {"color": "#2563EB"}}
    ))
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=30, b=10))
    return fig

def build_engagement_heatmap(df: pd.DataFrame) -> go.Figure:
    heat = df.pivot_table(index='Activity_Status', columns='Credit_Card_Status', values='Exited', aggfunc=lambda x: x.mean() * 100)
    fig = px.imshow(heat, text_auto='.1f', color_continuous_scale='YlOrRd', template='plotly_white', aspect='auto')
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig

# ---------------------------------------------------------
# TAB 4: HIGH-VALUE CAPITAL RISK EXPLORER (4 Visuals)
# ---------------------------------------------------------
def build_high_value_quadrant_matrix(df: pd.DataFrame) -> go.Figure:
    sample_df = df.sample(min(1500, len(df)), random_state=42)
    med_sal = df['EstimatedSalary'].median()
    med_bal = df['Balance'].median()
    
    fig = px.scatter(
        sample_df,
        x='EstimatedSalary',
        y='Balance',
        color='Churn_Status',
        color_discrete_map={'Retained (Active)': '#94A3B8', 'Churned (Exited)': '#EF4444'},
        opacity=0.7,
        template='plotly_white'
    )
    fig.add_vline(x=med_sal, line_dash="dot", line_color="#CBD5E1")
    fig.add_hline(y=med_bal, line_dash="dot", line_color="#CBD5E1")
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig

def build_zero_vs_funded_donut(df: pd.DataFrame) -> go.Figure:
    zf = df.groupby('Balance_Segment')['Exited'].agg(
        Total='count',
        Churned='sum',
        Churn_Rate=lambda x: x.mean() * 100
    ).reset_index()
    
    fig = px.bar(
        zf,
        x='Balance_Segment',
        y='Churn_Rate',
        color='Balance_Segment',
        text=zf['Churn_Rate'].apply(lambda x: f"{x:.1f}%"),
        color_discrete_sequence=['#94A3B8', '#3B82F6', '#EF4444'],
        template='plotly_white'
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), showlegend=False, yaxis=dict(title="Churn Rate (%)"))
    return fig

def build_top_decile_loss_bar(df: pd.DataFrame) -> go.Figure:
    df_ranked = df.copy()
    if len(df_ranked) < 10:
        df_ranked['Balance_Decile'] = 'D1'
    else:
        # Rank values with method='first' to resolve identical 0.0 balance bin edges
        df_ranked['Balance_Rank'] = df_ranked['Balance'].rank(method='first')
        df_ranked['Balance_Decile'] = pd.qcut(
            df_ranked['Balance_Rank'], 
            q=10, 
            labels=[f"D{i}" for i in range(1, 11)]
        )
    
    decile_summary = df_ranked.groupby('Balance_Decile', observed=False).agg(
        Lost_Balance=('Balance', lambda x: df_ranked.loc[x.index[df_ranked.loc[x.index, 'Exited'] == 1], 'Balance'].sum()),
        Churn_Rate=('Exited', lambda x: x.mean() * 100)
    ).reset_index()
    
    fig = px.bar(
        decile_summary,
        x='Balance_Decile',
        y='Lost_Balance',
        color='Churn_Rate',
        color_continuous_scale='Reds',
        template='plotly_white',
        labels={
            'Balance_Decile': 'Balance Decile (D1=Lowest, D10=Highest)',
            'Lost_Balance': 'Lost Capital (€)',
            'Churn_Rate': 'Churn Rate (%)'
        }
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Capital Lost (€)")
    )
    return fig

def build_tenure_high_value_bar(df: pd.DataFrame) -> go.Figure:
    hv_df = df[df['Balance'] > 50000]
    hv_tenure = hv_df.groupby(['Tenure_Group', 'Geography'], observed=False)['Exited'].mean().reset_index()
    hv_tenure['Churn_Rate'] = hv_tenure['Exited'] * 100
    
    fig = px.bar(
        hv_tenure,
        x='Tenure_Group',
        y='Churn_Rate',
        color='Geography',
        barmode='group',
        color_discrete_sequence=['#2563EB', '#EF4444', '#F59E0B'],
        template='plotly_white'
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), yaxis=dict(title="High-Value Churn (%)"))
    return fig

# ---------------------------------------------------------
# TAB 5: RETENTION & SCENARIO ENGINE (4 Visuals)
# ---------------------------------------------------------
def build_retention_waterfall(sim_results: dict) -> go.Figure:
    fig = go.Figure(go.Waterfall(
        name="Capital Preservation Bridge",
        orientation="v",
        x=["Baseline Capital at Risk", "German Intervention", "Age 46–60 Campaign", "Product Cross-Sell", "Simulated Capital Loss"],
        y=[
            sim_results['base_capital_loss'],
            -sim_results['german_saved_bal'],
            -sim_results['midage_saved_bal'],
            -sim_results['cross_sell_saved_bal'],
            0
        ],
        measure=["relative", "relative", "relative", "relative", "total"],
        decreasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#EF4444"}}
    ))
    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=30, b=10), yaxis=dict(title="Capital (€)"))
    return fig

def build_retention_sensitivity_heatmap(df: pd.DataFrame) -> go.Figure:
    germany_rates = np.linspace(5, 30, 6)
    midage_rates = np.linspace(5, 30, 6)
    
    ger_base = df[(df['Geography'] == 'Germany') & (df['Exited'] == 1)]['Balance'].sum()
    mid_base = df[(df['Age_Group'] == '46–60') & (df['Exited'] == 1)]['Balance'].sum()
    
    matrix = np.zeros((len(midage_rates), len(germany_rates)))
    for i, m in enumerate(midage_rates):
        for j, g in enumerate(germany_rates):
            matrix[i, j] = (ger_base * g / 100.0 + mid_base * m / 100.0) / 1e6
            
    fig = px.imshow(
        matrix,
        x=[f"{g:.0f}% Ger" for g in germany_rates],
        y=[f"{m:.0f}% Age" for m in midage_rates],
        labels=dict(x="German Retention Target", y="Age 46–60 Target", color="Preserved Capital (€M)"),
        color_continuous_scale="Greens",
        template="plotly_white",
        aspect="auto"
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig

def build_product_migration_model(df: pd.DataFrame) -> go.Figure:
    migrations = [0, 10, 20, 30, 40, 50]
    proj_churn = []
    base_churn = df['Exited'].mean() * 100
    single_p = len(df[df['NumOfProducts'] == 1])
    
    for m in migrations:
        saved = single_p * (m / 100.0) * (0.2771 - 0.0758)
        sim_c = (df['Exited'].sum() - saved) / len(df) * 100
        proj_churn.append(sim_c)
        
    fig = px.line(
        x=migrations,
        y=proj_churn,
        markers=True,
        labels={'x': '1-Product to 2-Product Cross-Sell Migration (%)', 'y': 'Projected Portfolio Churn (%)'},
        template='plotly_white'
    )
    fig.add_hline(y=15.0, line_dash="dash", line_color="#10B981", annotation_text="15% ECB Target")
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig

def build_regulatory_gauge(sim_churn: float, base_churn: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sim_churn,
        delta={'reference': base_churn, 'valueformat': '.2f', 'suffix': '%'},
        title={'text': "Simulated Churn vs Baseline (%)"},
        gauge={
            'axis': {'range': [0, 35]},
            'bar': {'color': "#2563EB"},
            'steps': [
                {'range': [0, 15], 'color': "#DCFCE7"},
                {'range': [15, 22], 'color': "#FEF3C7"},
                {'range': [22, 35], 'color': "#FEE2E2"}
            ],
            'threshold': {'line': {'color': "#EF4444", 'width': 4}, 'thickness': 0.75, 'value': 15.0}
        }
    ))
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), height=320)
    return fig