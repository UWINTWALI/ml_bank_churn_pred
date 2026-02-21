# File upload handling
import streamlit as st
import pandas as pd

# Exact columns the model pipeline expects (order matters for predict_proba)
MODEL_FEATURES = [
    "customerid", "creditscore", "geography", "gender", "age",
    "tenure", "balance", "numofproducts", "hascrcard",
    "isactivemember", "estimatedsalary",
]

def handle_file_upload():
    """Handle CSV upload with validation.

    Returns
    -------
    tuple : (df | None, filename | None, error_code | None)
        error_code is "no_features" when the file contains none of the
        required model columns; None means no error occurred.
    """
    uploaded_file = st.file_uploader("Upload customer CSV", type='csv')

    if uploaded_file is not None:
        try:
            raw = pd.read_csv(uploaded_file)

            # Normalise column names to lower-case so matching is case-insensitive
            raw.columns = [c.strip().lower() for c in raw.columns]

            # Keep only the columns the model needs, in the right order
            available = [c for c in MODEL_FEATURES if c in raw.columns]

            if not available:
                # None of the required features exist – signal the caller
                return None, uploaded_file.name, "no_features"

            df = raw[available]
            return df, uploaded_file.name, None

        except Exception as e:
            st.error(str(e))
            return None, None, None

    return None, None, None


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
