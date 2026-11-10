# ============================================================
# DATA PREPROCESSING
# ============================================================

import pandas as pd


def clean_data(df, subject_columns):
    """
    Clean and validate student performance data.
    """

    print("\n========== DATA CLEANING ==========")

    # Remove duplicate rows
    duplicate_count = df.duplicated().sum()

    print("Duplicate rows found:", duplicate_count)

    df = df.drop_duplicates().copy()

    # Check missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Check subject marks
    print("\nSubject mark ranges:")

    for column in subject_columns:
        print(
            column,
            "Min:", df[column].min(),
            "Max:", df[column].max()
        )

    # Check attendance
    print("\nAttendance range:")

    print(
        "Min:",
        df["Attendance_Percent"].min()
    )

    print(
        "Max:",
        df["Attendance_Percent"].max()
    )

    # Remove invalid marks
    valid_marks = (
        (df[subject_columns] >= 0).all(axis=1)
        &
        (df[subject_columns] <= 100).all(axis=1)
    )

    # Remove invalid attendance
    valid_attendance = (
        (df["Attendance_Percent"] >= 0)
        &
        (df["Attendance_Percent"] <= 100)
    )

    df = df[
        valid_marks & valid_attendance
    ].copy()

    return df


def create_average_marks(df, subject_columns):
    """
    Calculate average marks across all subjects.
    """

    df["Average_Marks"] = df[
        subject_columns
    ].mean(axis=1)

    return df


def create_performance_band(df):
    """
    Create performance categories.
    """

    bins = [
        -1,
        39,
        49,
        59,
        69,
        79,
        89,
        100
    ]

    labels = [
        "Below 40",
        "40-49",
        "50-59",
        "60-69",
        "70-79",
        "80-89",
        "90-100"
    ]

    df["Performance_Band"] = pd.cut(
        df["Average_Marks"],
        bins=bins,
        labels=labels
    )

    return df


def create_attendance_band(df):
    """
    Create attendance categories.
    """

    bins = [
        -1,
        74.99,
        84.99,
        94.99,
        100
    ]

    labels = [
        "Below 75%",
        "75-84%",
        "85-94%",
        "95-100%"
    ]

    df["Attendance_Band"] = pd.cut(
        df["Attendance_Percent"],
        bins=bins,
        labels=labels
    )

    return df


def create_age_group(df):
    """
    Create age groups.
    """

    bins = [
        0,
        13,
        15,
        17,
        100
    ]

    labels = [
        "12 or below",
        "14-15",
        "16-17",
        "18+"
    ]

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=bins,
        labels=labels
    )

    return df