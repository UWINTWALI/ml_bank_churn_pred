import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.file_utils import handle_file_upload
from utils.kpi_calculator import calculate_kpis


class Batch:
    def __init__(self, model_data):
        self.pipeline = model_data["pipeline"]
        self.threshold = model_data["threshold"]
        # self.pipeline, self.threshold, _, _ = model_data

    def render(self):
        st.markdown("# Batch Predictions")

        df, filename = handle_file_upload()
        if df is not None:
            probs = self.pipeline.predict_proba(df)[:, 1]
            preds = (probs > self.threshold).astype(int)
            df['churn_prob'] = list(probs)
            df['prediction'] = preds
            # Save to session for other pages if desired
            st.session_state['pred_df'] = df

            # Sidebar filter
            with st.sidebar:
                min_prob = st.slider("Show High Risk >", 0.0, 1.0, 0.3)
                df_filtered = df[df['churn_prob'] > min_prob]

            # KPIs
            kpis = calculate_kpis(df_filtered, df_filtered['prediction'])
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Customers", kpis['total'])
            col2.metric("High Risk", kpis['churners'])
            col3.metric("Rate", f"{kpis['rate']:.1%}")
            col4.metric("Value", f"${kpis['net_value']:,.0f}")

            st.write(f"Total Records: {len(df)} | Filtered Records: {len(df_filtered)}")

            # Display all columns with prediction and probability at the end, excluding churn_prob from middle
            display_cols = [col for col in df_filtered.columns if col not in ['prediction', 'churn_prob']] + ['churn_prob', 'prediction']
            st.dataframe(df_filtered[display_cols], use_container_width=True)
            st.download_button("Download", df.to_csv(index=False).encode(), f"{filename}_results.csv")

            # VISUALS: show plots derived from the predicted file in a compact two-column grid
            st.header('Visualizations from Predicted File')

            # determine churn column
            if 'prediction' in df.columns:
                churn_col = 'prediction'
            elif 'exited_pred' in df.columns:
                churn_col = 'exited_pred'
            else:
                churn_col = None

            plots = []

            # churn count (small)
            if churn_col is not None:
                churn_counts = df[churn_col].value_counts().reindex([0, 1], fill_value=0)
                fig_count, ax_count = plt.subplots(figsize=(5, 3))
                sns.countplot(x=churn_col, data=df, ax=ax_count, palette='Set2')
                ax_count.set_title('Customer Churn Distribution')
                ax_count.set_xlabel('Churn Status')
                ax_count.set_ylabel('Number of Customers')
                for p in ax_count.patches:
                    ax_count.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=9)
                plots.append(fig_count)

                # churn pie
                fig_pie, ax_pie = plt.subplots(figsize=(5, 3))
                labels = ['Retained', 'Churned']
                sizes = [churn_counts.get(0, 0), churn_counts.get(1, 0)]
                ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral'], explode=(0, 0.05), textprops={'fontsize': 9})
                ax_pie.set_title('Churn Rate Percentage')
                plots.append(fig_pie)

            # churn by age groups
            if 'age' in df.columns and churn_col is not None:
                bins = [0, 20, 30, 40, 50, 60, 70, 100]
                labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71+']
                df['Age_Group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
                age_churn = df.groupby('Age_Group')[churn_col].mean() * 100
                fig_age, ax_age = plt.subplots(figsize=(5, 3))
                age_churn.plot(kind='bar', color='steelblue', ax=ax_age)
                ax_age.set_title('Churn Rate by Age Group (%)')
                ax_age.set_xlabel('Age Group')
                ax_age.set_ylabel('Churn Rate (%)')
                for p in ax_age.patches:
                    ax_age.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=9)
                plots.append(fig_age)

            # churn by balance (binned)
            balance_col = None
            if 'balance' in df.columns:
                balance_col = 'balance'
            elif 'Balance' in df.columns:
                balance_col = 'Balance'

            if balance_col is not None and churn_col is not None:
                # create sensible bins based on distribution
                max_bal = int(df[balance_col].max(skipna=True) if pd.api.types.is_numeric_dtype(df[balance_col]) else 0)
                bins = [0, 5000, 15000, 30000, 60000, 100000, max_bal + 1]
                labels = ['0-5k', '5k-15k', '15k-30k', '30k-60k', '60k-100k', '100k+']
                try:
                    df['Balance_Group'] = pd.cut(df[balance_col], bins=bins, labels=labels, include_lowest=True)
                    bal_churn = df.groupby('Balance_Group')[churn_col].mean() * 100
                    fig_bal, ax_bal = plt.subplots(figsize=(5, 3))
                    bal_churn.plot(kind='bar', color='indianred', ax=ax_bal)
                    ax_bal.set_title('Churn Rate by Balance Group (%)')
                    ax_bal.set_xlabel('Balance Group')
                    ax_bal.set_ylabel('Churn Rate (%)')
                    for p in ax_bal.patches:
                        ax_bal.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=9)
                    plots.append(fig_bal)
                except Exception:
                    # if binning fails, skip gracefully
                    pass
            # churn by balance groups
            if 'balance' in df.columns and churn_col is not None:
                # Create balance quartile groups safely (handle duplicate edges)
                try:
                    bal_q = pd.qcut(df['balance'], q=4, duplicates='drop')
                    # build labels based on number of bins returned
                    cats = list(bal_q.cat.categories)
                    labels = []
                    for i in range(len(cats)):
                        if i == 0:
                            labels.append(f'Q{i+1} (Low)')
                        elif i == len(cats) - 1:
                            labels.append(f'Q{i+1} (High)')
                        else:
                            labels.append(f'Q{i+1}')
                    # map category intervals to labels
                    mapping = {cat: lbl for cat, lbl in zip(cats, labels)}
                    df['Balance_Quartile'] = bal_q.map(mapping)
                    # ensure categorical order
                    df['Balance_Quartile'] = pd.Categorical(df['Balance_Quartile'], categories=labels, ordered=True)
                except Exception:
                    # fallback: equal-width bins
                    try:
                        max_bal = float(df['balance'].max(skipna=True))
                        bins = [0, max_bal*0.25, max_bal*0.5, max_bal*0.75, max_bal]
                        df['Balance_Quartile'] = pd.cut(df['balance'], bins=bins, include_lowest=True)
                        df['Balance_Quartile'] = df['Balance_Quartile'].astype(str)
                    except Exception:
                        df['Balance_Quartile'] = 'Unknown'

                balance_churn = df.groupby('Balance_Quartile')[churn_col].mean() * 100

                fig_balance, ax_balance = plt.subplots(figsize=(5, 3))
                bars = ax_balance.bar(balance_churn.index.astype(str), balance_churn.values,
                                     color=['skyblue'] * len(balance_churn))
                ax_balance.set_title('Churn Rate by Balance Quartile (%)')
                ax_balance.set_xlabel('Balance Quartile')
                ax_balance.set_ylabel('Churn Rate (%)')
                ax_balance.tick_params(axis='x', rotation=0)

                for bar, rate in zip(bars, balance_churn.values):
                    ax_balance.annotate(f'{rate:.1f}%',
                                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                                        ha='center', va='bottom', fontsize=9)

                plots.append(fig_balance)

            # Numeric distributions
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            numeric_cols = [c for c in numeric_cols if c not in ['churn_prob', 'prediction']]
            if numeric_cols:
                st.subheader('Numeric Feature Distributions')
                sel = st.multiselect('Select numeric columns to visualize', numeric_cols, default=numeric_cols[:4])
                for col in sel:
                    fig_hist, ax_hist = plt.subplots(figsize=(5, 3))
                    sns.histplot(df[col].dropna(), kde=True, ax=ax_hist)
                    ax_hist.set_title(f'Distribution of {col}')
                    plots.append(fig_hist)

            # Render plots in a two-column grid
            for i in range(0, len(plots), 2):
                cols = st.columns(2)
                with cols[0]:
                    st.pyplot(plots[i])
                if i + 1 < len(plots):
                    with cols[1]:
                        st.pyplot(plots[i + 1])
