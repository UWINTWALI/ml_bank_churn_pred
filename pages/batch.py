import streamlit as st
from utils.file_utils import handle_file_upload
from utils.kpi_calculator import calculate_kpis

class Batch:
    def __init__(self, model_data):
        self.pipeline, self.threshold, _, _ = model_data
    
    def render(self):
        st.markdown("# Batch Predictions")
        
        df, filename = handle_file_upload()
        if df is not None:
            probs = self.pipeline.predict_proba(df)[:, 1]
            preds = (probs > self.threshold).astype(int)
            df['churn_prob'] = probs
            df['prediction'] = preds
            
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
            
            st.dataframe(df_filtered[['churn_prob', 'prediction']])
            st.download_button("Download", df.to_csv(index=False).encode(), f"{filename}_results.csv")
