import streamlit as st
from streamlit_option_menu import option_menu
import pages
import utils.model_utils

# Config
st.set_page_config(page_title="Churn Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass  # No CSS? Continue

# Global model
@st.cache_resource
def get_model():
    return utils.model_utils.load_churn_model()

model_data = get_model()
pipeline, threshold, feature_names, metrics = model_data

# Navigation
with st.sidebar:
    st.markdown("## Churn Dashboard")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Prediction", "Batch", "Metrics", "Insights"],
        icons=["bar-chart", "person", "table", "graph-up", "lightbulb"],
        menu_icon="cast",
        default_index=0,
    )

# Page map - FIXED imports
page_map = {
    "Dashboard": pages.Dashboard(model_data).render,
    "Prediction": pages.Prediction(model_data).render, 
    "Batch": pages.Batch(model_data).render,
    "Metrics": pages.Metrics(model_data).render,
    "Insights": pages.Insights(model_data).render,
}
# Render page
page_map[selected]()