"""
Batch analysis page for churn prediction app
"""

import streamlit as st
import pandas as pd
from utils.predictor import make_batch_predictions
from utils.file_utils import handle_csv_upload


def render_batch_analysis_page():
    """Render the batch analysis page"""
    st.markdown("<h2 class='section-header'> Batch Analysis</h2>", unsafe_allow_html=True)
    
    if not st.session_state.get('models_trained', False):
        st.warning(" Pipeline not loaded. Please load the pipeline first.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("###  Data Upload")
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key="batch_upload")
        
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.session_state.batch_data = data
            st.success(f" Loaded {len(data)} records")
    
    with col2:
        st.markdown("### Analysis Results")
        
        if 'batch_data' in st.session_state:
            data = st.session_state.batch_data
            
            st.info(f"Processing: **{uploaded_file.name if uploaded_file else 'data'}** ({len(data)} rows)")
            
            # Show preview
            with st.expander("Preview Data", expanded=False):
                st.dataframe(data.head(10), use_container_width=True)
            
            if st.button("🔍 Run Batch Analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing customers..."):
                    results = make_batch_predictions(data, st.session_state)
                
                if results is not None:
                    st.session_state.batch_results = results
                    
                    # Summary
                    st.markdown("---")
                    st.markdown("#### Summary Statistics")
                    
                    total_customers = len(results)
                    high_risk = (results['prediction'] == 'High Risk').sum()
                    high_risk_pct = (high_risk / total_customers * 100) if total_customers > 0 else 0
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Analyzed", total_customers)
                    with col_b:
                        st.metric("High Risk", high_risk)
                    with col_c:
                        st.metric("High Risk %", f"{high_risk_pct:.1f}%")
                    
                    # Results table
                    st.markdown("#### Detailed Results")
                    st.dataframe(results.head(50), use_container_width=True)
                    
                    # Download
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="Download Results (CSV)",
                        data=csv,
                        file_name="churn_predictions.csv",
                        mime="text/csv"
                    )
        else:
            st.info("Upload a CSV file from the left panel to start analysis")
