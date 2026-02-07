# Data validation and preprocessing
import pandas as pd

REQUIRED_COLS = [
    'creditscore', 'geography', 'gender', 'age', 'tenure',
    'balance', 'numofproducts', 'hascrcard', 'isactivemember', 'estimatedsalary'
]

def validate_customer_data(data_dict):
    """Convert dict to validated DataFrame"""
    df = pd.DataFrame([data_dict])
    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df[REQUIRED_COLS]

def validate_batch_data(df):
    """Validate uploaded CSV"""
    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df[REQUIRED_COLS].copy()
