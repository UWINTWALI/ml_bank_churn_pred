"""
Prediction utilities for single and batch predictions
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import joblib
import traceback

def load_models_and_preprocessor():
    """
    Load trained models and preprocessor from saved files
    """
    try:
        # Try to load the pre-trained pipeline (if saved)
        if os.path.exists('models/full_pipeline.pkl'):
            pipeline = joblib.load('models/full_pipeline.pkl')
            print("✓ Loaded full pipeline from models/full_pipeline.pkl")
            return {'pipeline': pipeline}
        
        # Fallback: Load individual components
        preprocessor = joblib.load('models/preprocessor.pkl')
        model_phase1 = joblib.load('models/model_phase1.pkl')
        
        # Check if phase2 model exists
        model_phase2 = None
        if os.path.exists('models/model_phase2.pkl'):
            model_phase2 = joblib.load('models/model_phase2.pkl')
        
        print("✓ Loaded individual model components")
        return {
            'preprocessor': preprocessor,
            'model_phase1': model_phase1,
            'model_phase2': model_phase2
        }
        
    except Exception as e:
        st.error(f"Error loading models: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return None

def _get_feature_names_from_preprocessor(preprocessor):
    """
    Extract feature names from the preprocessor
    """
    try:
        # Get numerical columns from the preprocessor
        numerical_cols = preprocessor.named_transformers_['num'].feature_names_in_
        
        # Get categorical columns and their encoded names
        categorical_encoder = preprocessor.named_transformers_['cat']
        categorical_features = categorical_encoder.get_feature_names_out()
        
        # Combine all feature names
        feature_names = list(numerical_cols) + list(categorical_features)
        return feature_names
        
    except Exception as e:
        print(f"Error extracting feature names: {e}")
        return None

def _diagnose_pipeline_error(pipeline, data, err):
    """Detailed error diagnostics for pipeline issues"""
    st.error(f"**Pipeline Error:** {str(err)}")
    
    with st.expander("View Error Details"):
        st.write("### Pipeline Structure")
        if hasattr(pipeline, 'named_steps'):
            for name, step in pipeline.named_steps.items():
                st.write(f"**Step '{name}':** {type(step).__name__}")
        
        st.write("### Input Data Info")
        st.write(f"**Shape:** {data.shape}")
        st.write("**Columns:**", list(data.columns))
        st.write("**Data types:**")
        st.write(data.dtypes)
        
        st.write("### Sample Input Data")
        st.dataframe(data.head())

def _prepare_input_data(customer_data, expected_features=None):
    """
    Prepare input data ensuring correct column order and types
    """
    # Convert to DataFrame if it's a dictionary
    if isinstance(customer_data, dict):
        df = pd.DataFrame([customer_data])
    else:
        df = customer_data.copy()
    
    # Ensure correct column order if expected_features is provided
    if expected_features is not None:
        # Keep only columns that are in expected features
        df = df.reindex(columns=expected_features, fill_value=0)
    
    return df

def make_single_prediction(customer_data, session_state):
    """
    Make churn prediction for a single customer
    
    Args:
        customer_data: Dictionary or DataFrame with customer features
        session_state: Streamlit session state with models
    
    Returns:
        Dictionary with prediction results
    """
    try:
        # Check which model format we have
        pipeline = session_state.get('pipeline', None)
        preprocessor = session_state.get('preprocessor', None)
        model_phase1 = session_state.get('model_phase1', None)
        
        if pipeline is not None:
            # Use full pipeline (handles preprocessing + prediction)
            try:
                # Prepare input data
                input_df = _prepare_input_data(customer_data)
                
                # Get prediction probabilities
                proba = pipeline.predict_proba(input_df)[0, 1]
                threshold = session_state.get('threshold', 0.4)
                churn_pred = int(proba >= threshold)
                
                return {
                    'prediction': 'High Risk' if churn_pred == 1 else 'Low Risk',
                    'probability': float(proba),
                    'churn_probability': float(proba),
                    'churn_prediction': churn_pred,
                    'risk_level': 'high' if churn_pred == 1 else 'low',
                    'confidence': 'high' if proba >= 0.7 or proba <= 0.3 else 'medium'
                }
            except Exception as e:
                _diagnose_pipeline_error(pipeline, input_df, e)
                return None
        
        elif preprocessor is not None and model_phase1 is not None:
            # Use separate preprocessor and models
            try:
                # Prepare input data
                input_df = _prepare_input_data(customer_data)
                
                # Transform data
                X_processed = preprocessor.transform(input_df)
                
                # Phase 1 prediction
                proba_phase1 = model_phase1.predict_proba(X_processed)[0, 1]
                threshold = session_state.get('threshold', 0.4)
                
                # Check if we need phase 2
                model_phase2 = session_state.get('model_phase2', None)
                
                if proba_phase1 >= threshold and model_phase2 is not None:
                    # Use phase 2 for confirmation
                    proba_phase2 = model_phase2.predict_proba(X_processed)[0, 1]
                    final_prediction = 'High Risk' if proba_phase2 >= 0.5 else 'Low Risk'
                    final_probability = proba_phase2
                else:
                    final_prediction = 'High Risk' if proba_phase1 >= threshold else 'Low Risk'
                    final_probability = proba_phase1
                
                return {
                    'prediction': final_prediction,
                    'probability': float(final_probability),
                    'churn_probability': float(final_probability),
                    'churn_prediction': 1 if final_prediction == 'High Risk' else 0,
                    'risk_level': 'high' if final_prediction == 'High Risk' else 'low',
                    'confidence': 'high' if final_probability >= 0.7 or final_probability <= 0.3 else 'medium'
                }
            except Exception as e:
                st.error(f"Prediction error: {e}")
                print(f"Error details: {traceback.format_exc()}")
                return None
        else:
            st.error("No trained models found in session state")
            return None
            
    except Exception as e:
        st.error(f"Unexpected error in prediction: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return None

def make_batch_predictions(data, session_state):
    """
    Make predictions for multiple customers
    
    Args:
        data: DataFrame with customer features
        session_state: Streamlit session state with models
    
    Returns:
        DataFrame with predictions
    """
    try:
        # Check which model format we have
        pipeline = session_state.get('pipeline', None)
        preprocessor = session_state.get('preprocessor', None)
        model_phase1 = session_state.get('model_phase1', None)
        
        if pipeline is not None:
            # Use full pipeline
            try:
                proba = pipeline.predict_proba(data)[:, 1]
                threshold = session_state.get('threshold', 0.4)
                churn_pred = (proba >= threshold).astype(int)
                
                results = data.copy()
                results['churn_probability'] = proba
                results['churn_prediction'] = churn_pred
                results['prediction'] = results['churn_prediction'].map({1: 'High Risk', 0: 'Low Risk'})
                
                # Add risk score
                def get_risk_score(prob):
                    if prob >= 0.7:
                        return 'Very High'
                    elif prob >= 0.4:
                        return 'High'
                    elif prob >= 0.3:
                        return 'Medium'
                    else:
                        return 'Low'
                
                results['risk_score'] = results['churn_probability'].apply(get_risk_score)
                
                return results
            except Exception as e:
                _diagnose_pipeline_error(pipeline, data, e)
                return None
        
        elif preprocessor is not None and model_phase1 is not None:
            # Use separate components
            X_processed = preprocessor.transform(data)
            
            # Phase 1 predictions
            proba_phase1 = model_phase1.predict_proba(X_processed)[:, 1]
            threshold = session_state.get('threshold', 0.4)
            
            # Initialize results
            final_predictions = []
            final_probabilities = []
            
            # Check if phase 2 is available
            model_phase2 = session_state.get('model_phase2', None)
            
            for i, prob in enumerate(proba_phase1):
                if prob >= threshold and model_phase2 is not None:
                    # Get phase 2 prediction
                    prob_phase2 = model_phase2.predict_proba(X_processed[i:i+1])[0, 1]
                    final_pred = 'High Risk' if prob_phase2 >= 0.5 else 'Low Risk'
                    final_prob = prob_phase2
                else:
                    final_pred = 'High Risk' if prob >= threshold else 'Low Risk'
                    final_prob = prob
                
                final_predictions.append(final_pred)
                final_probabilities.append(final_prob)
            
            # Create results DataFrame
            results = data.copy()
            results['churn_probability'] = final_probabilities
            results['prediction'] = final_predictions
            results['churn_prediction'] = results['prediction'].map({'High Risk': 1, 'Low Risk': 0})
            
            # Add risk score
            def get_risk_score(prob):
                if prob >= 0.7:
                    return 'Very High'
                elif prob >= 0.4:
                    return 'High'
                elif prob >= 0.3:
                    return 'Medium'
                else:
                    return 'Low'
            
            results['risk_score'] = results['churn_probability'].apply(get_risk_score)
            
            return results
        
        else:
            st.error("No trained models found in session state")
            return None
            
    except Exception as e:
        st.error(f"Batch prediction error: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return None