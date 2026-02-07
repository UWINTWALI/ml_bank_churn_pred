import streamlit as st

class Insights:
    def __init__(self, model_data):
        self.model_data = model_data
    
    def render(self):
        st.markdown("# Business Insights")
        
        st.markdown("""
        ### **Key Findings**
        - **Germany customers**: 2x churn risk
        - **Age 35-45**: Peak churn window  
        - **High balance + inactive**: Danger zone
        
        ### **ROI Analysis**
        | Campaign Size | Cost     | Expected Value | Net Profit |
        |---------------|----------|----------------|------------|
        | Top 500       | $100K    | $400K          | **$300K**  |
        | Top 1000      | $200K    | $676K          | **$476K**  |
        
        ### **Action Plan**
        1. Target top 20% risk customers first
        2. Budget: $200K for maximum ROI
        3. Expected: Save 300+ customers
        """)
