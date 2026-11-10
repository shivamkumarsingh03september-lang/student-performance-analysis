# ============================================================
# DATA LOADER
# ============================================================

import pandas as pd


def load_data(file_path):
    """
    Load student performance CSV file.
    """

    df = pd.read_csv(file_path)

    return df


def inspect_data(df):
    """
    Display basic information about the dataset.
    """

    print("\n========== DATASET INFORMATION ==========")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nStatistical Summary:")
    print(df.describe(include="all"))