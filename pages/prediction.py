import streamlit as st
from utils.data_loader import validate_customer_data

class Prediction:
    def __init__(self, model_data):
        self.pipeline = model_data["pipeline"]
        self.threshold = model_data["threshold"]
        # self.pipeline, self.threshold, _, _ = model_data
        
    
    def render(self):
        st.markdown("# Single Customer Prediction")
        
        # Sidebar filters
        with st.sidebar:
            st.header("Filters")
            age_range = st.slider("Age", 18, 90, (25, 60))
        
        # Inputs
        col1, col2 = st.columns(2)
        with col1:
            creditscore = st.number_input("Credit Score", min_value=300, max_value=850, value=650)
            age = st.number_input("Age", min_value=age_range[0], max_value=age_range[1], value=40)
            balance = st.number_input("Balance", min_value=0.0, max_value=250000.0, value=80000.0)
        with col2:
            tenure = st.number_input("Tenure", min_value=0, max_value=10, value=4)
            products = st.number_input("Products", min_value=1, max_value=4, value=2)
            salary = st.number_input("Salary", min_value=0.0, max_value=200000.0, value=100000.0)
        
        col1, col2, col3 = st.columns(3)
        with col1: geo = st.selectbox("Geography", ['France', 'Spain', 'Germany'])
        with col2: gender = st.selectbox("Gender", ['Female', 'Male'])
        with col3: active = st.selectbox("Active", [1, 0])
        
        if st.button("Predict", type="primary", use_container_width=True):
            data = validate_customer_data({
                'creditscore': creditscore, 'geography': geo, 'gender': gender,
                'age': age, 'tenure': tenure, 'balance': balance,
                'numofproducts': products, 'hascrcard': 1, 'isactivemember': active,
                'estimatedsalary': salary
            })
            
            prob = self.pipeline.predict_proba(data)[0, 1]
            pred = 1 if prob > self.threshold else 0
            
            # Inline result banner shown right below the Predict button
            if pred:
                st.error(
                    "Due to high risk, Customer might Churn!",
                    icon=":material/warning:"
                )
            else:
                st.success(
                    "Due to low risk, Customer is not likely to Churn!",
                    icon=":material/check_circle:"
                )

            # Probability metric shown alongside the banner
            st.metric("Churn Probability", f"{prob:.1%}")