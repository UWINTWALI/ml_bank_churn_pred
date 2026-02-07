# Clean model loading with exact notebook structure
import joblib
import streamlit as st

def load_churn_model():
    """Load churn model with exact notebook structure"""
    try:
        model_data = joblib.load('models/churn_pipeline.pkl')
        return (
            model_data['pipeline'],           # sklearn pipeline
            model_data['threshold'],          # 0.4
            model_data['feature_names'],      # processed feature names
            model_data['metrics']             # model performance
        )
    except FileNotFoundError:
        st.error(" Run notebook first: `joblib.dump({'pipeline': churn_pipeline, ...})`")
        st.stop()
    except KeyError as e:
        st.error(f" Model missing key: {e}")
        st.stop()
