import streamlit as st
from streamlit_option_menu import option_menu
import pages
import utils.model_utils

# Config
st.set_page_config(
    page_title="Churn Prediction Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Global model
@st.cache_resource
def get_model():
    return utils.model_utils.load_churn_model()

model_data = get_model()

# Optional direct access (not required, but safe)
pipeline = model_data["pipeline"]
threshold = model_data["threshold"]
feature_names = model_data["feature_names"]
metrics = model_data["metrics"]

# Navigation
with st.sidebar:
    st.markdown("## Churn Prediction Dashboard Menu")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Single User Prediction", "Mass Prediction", "Metrics", "Insights"],
        icons=["bar-chart", "person", "table", "graph-up", "lightbulb"],
        menu_icon="cast",
        default_index=0,
    )

# Page map
page_map = {
    "Dashboard": pages.Dashboard(model_data).render,
    "Single User Prediction": pages.Prediction(model_data).render,
    "Mass Prediction": pages.Batch(model_data).render,
    "Metrics": pages.Metrics(model_data).render,
    "Insights": pages.Insights(model_data).render,
}

# Render page
page_map[selected]()
