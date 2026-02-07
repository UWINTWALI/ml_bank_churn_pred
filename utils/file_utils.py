# File upload handling
import streamlit as st
import pandas as pd

def handle_file_upload():
    """Handle CSV upload with validation"""
    uploaded_file = st.file_uploader("Upload customer CSV", type='csv')
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df, uploaded_file.name
        except Exception as e:
            st.error(str(e))
            return None, None
    return None, None


def handle_csv_upload(uploaded_file):
    """Handle CSV upload and return data, row count, and success status"""
    try:
        if uploaded_file is None:
            return None, 0, False
        
        data = pd.read_csv(uploaded_file)
        return data, len(data), True
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None, 0, False
