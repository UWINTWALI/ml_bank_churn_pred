# ============================================================================
# REUSABLE MISSING VALUES HANDLER
# ============================================================================

import pandas as pd
import numpy as np

def handle_missing(df, show_info=True):
    """
    A function to handle missing values in a DataFrame.
    
    Rules:
    1. Drop columns with >50% missing values
    2. Fill numeric columns with median
    3. Fill categorical columns with mode
    4. Drop any remaining rows with missing values (if few)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame
    show_info : bool
        Whether to print summary information
    
    Returns:
    --------
    pandas.DataFrame
        Cleaned DataFrame
    """
    
    # Create a copy
    df_clean = df.copy()
    
    if show_info:
        print(" CHECKING FOR MISSING VALUES")
        print("==" * 40)
    
    # Count missing values before
    missing_before = df_clean.isnull().sum().sum()
    
    if missing_before == 0:
        if show_info:
            print("WoW! There is NO missing values found")
        return df_clean
    
    # Show missing count per column
    missing_cols = df_clean.isnull().sum()
    missing_cols = missing_cols[missing_cols > 0]
    
    if show_info:
        print(f"Found {missing_before:,} missing values in {len(missing_cols)} columns:")
        for col in missing_cols.index:
            count = missing_cols[col]
            percent = (count / len(df_clean)) * 100
            dtype = df_clean[col].dtype
            print(f"  • {col}: {count:,} ({percent:.1f}%) - Type: {dtype}")
    
    # 1. Drop columns with too many missing values (>50%)
    cols_to_drop = []
    for col in missing_cols.index:
        missing_percent = (missing_cols[col] / len(df_clean)) * 100
        if missing_percent > 50:
            cols_to_drop.append(col)
    
    if cols_to_drop:
        df_clean = df_clean.drop(columns=cols_to_drop)
        if show_info:
            print(f"\nDropped {len(cols_to_drop)} columns (>50% missing):")
            for col in cols_to_drop:
                print(f"- {col}")
    
    # 2. Fill remaining missing values
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            # Check column type
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                # Fill numeric with median
                fill_value = df_clean[col].median()
                df_clean[col].fillna(fill_value, inplace=True)
                method = "median"
            else:
                # Fill categorical with mode (most common value)
                fill_value = df_clean[col].mode()[0] if not df_clean[col].mode().empty else "Unknown"
                df_clean[col].fillna(fill_value, inplace=True)
                method = "mode"
            
            if show_info:
                print(f"  • {col}: Filled with {method} ({fill_value})")
    
    # 3. Final check - drop any rows that still have missing values (should be very few)
    rows_with_missing = df_clean.isnull().any(axis=1).sum()
    if rows_with_missing > 0:
        if show_info:
            print(f"\n  {rows_with_missing} rows still have missing values - dropping them")
        df_clean = df_clean.dropna()
    
    # Summary
    if show_info:
        missing_after = df_clean.isnull().sum().sum()
        print(f"\n CLEANING COMPLETE")
        print(f"  - Missing before: {missing_before:,}")
        print(f"  - Missing after: {missing_after:,}")
        print(f"  - Remaining rows: {len(df_clean):,}")
        print(f"  - Remaining columns: {len(df_clean.columns)}")
    
    return df_clean
