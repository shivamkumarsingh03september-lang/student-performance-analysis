# ============================================================
# DATA ANALYSIS
# ============================================================

import pandas as pd


def overall_performance(df):
    """
    Calculate overall student performance.
    """

    result = {
        "Total Students": len(df),
        "Average Marks": round(
            df["Average_Marks"].mean(), 2
        ),
        "Average Attendance": round(
            df["Attendance_Percent"].mean(), 2
        ),
        "Minimum Marks": round(
            df["Average_Marks"].min(), 2
        ),
        "Maximum Marks": round(
            df["Average_Marks"].max(), 2
        )
    }

    return result


def performance_band_analysis(df):
    """
    Analyze performance bands.
    """

    result = (
        df["Performance_Band"]
        .value_counts()
        .sort_index()
    )

    return result


def attendance_analysis(df):
    """
    Analyze attendance.
    """

    result = {
        "Average Attendance": round(
            df["Attendance_Percent"].mean(), 2
        ),
        "Minimum Attendance": round(
            df["Attendance_Percent"].min(), 2
        ),
        "Maximum Attendance": round(
            df["Attendance_Percent"].max(), 2
        )
    }

    return result


def attendance_marks_correlation(df):
    """
    Calculate correlation between attendance
    and average marks.
    """

    correlation = df[
        [
            "Attendance_Percent",
            "Average_Marks"
        ]
    ].corr()

    value = correlation.loc[
        "Attendance_Percent",
        "Average_Marks"
    ]

    return round(value, 3)


def subject_analysis(df, subject_columns):
    """
    Subject-wise performance analysis.
    """

    result = []

    for subject in subject_columns:

        result.append({

            "Subject": subject,

            "Average": round(
                df[subject].mean(), 2
            ),

            "Median": round(
                df[subject].median(), 2
            ),

            "Minimum": round(
                df[subject].min(), 2
            ),

            "Maximum": round(
                df[subject].max(), 2
            ),

            "Pass_Rate": round(
                (df[subject] >= 40).mean() * 100,
                2
            ),

            "Below_40": int(
                (df[subject] < 40).sum()
            )
        })

    return pd.DataFrame(result)


def underperforming_subjects(
    subject_summary,
    threshold=50
):
    """
    Find subjects with average marks below
    the defined threshold.
    """

    result = subject_summary[
        subject_summary["Average"] < threshold
    ].sort_values("Average")

    return result


def class_analysis(df):
    """
    Class-wise performance analysis.
    """

    result = (
        df.groupby("Class")
        .agg(
            Students=("Student_ID", "count"),

            Avg_Attendance=(
                "Attendance_Percent",
                "mean"
            ),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            ),

            Median_Marks=(
                "Average_Marks",
                "median"
            )
        )
        .reset_index()
    )

    result["Avg_Attendance"] = result[
        "Avg_Attendance"
    ].round(2)

    result["Avg_Marks"] = result[
        "Avg_Marks"
    ].round(2)

    return result


def section_analysis(df):
    """
    Section-wise performance analysis.
    """

    result = (
        df.groupby(
            ["Class", "Section"]
        )
        .agg(
            Students=("Student_ID", "count"),

            Avg_Attendance=(
                "Attendance_Percent",
                "mean"
            ),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            )
        )
        .reset_index()
    )

    result["Avg_Attendance"] = result[
        "Avg_Attendance"
    ].round(2)

    result["Avg_Marks"] = result[
        "Avg_Marks"
    ].round(2)

    return result


def class_subject_analysis(
    df,
    subject_columns
):
    """
    Calculate subject performance by class.
    """

    return (
        df.groupby("Class")[subject_columns]
        .mean()
        .round(2)
        .reset_index()
    )


def attendance_band_analysis(df):
    """
    Compare attendance bands with average marks.
    """

    result = (
        df.groupby(
            "Attendance_Band",
            observed=False
        )
        .agg(
            Students=("Student_ID", "count"),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            )
        )
        .reset_index()
    )

    result["Avg_Marks"] = result[
        "Avg_Marks"
    ].round(2)

    return result


def gender_analysis(df):
    """
    Gender-wise descriptive analysis.
    """

    result = (
        df.groupby("Gender")
        .agg(
            Students=("Student_ID", "count"),

            Avg_Attendance=(
                "Attendance_Percent",
                "mean"
            ),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            )
        )
        .reset_index()
    )

    return result.round(2)


def age_analysis(df):
    """
    Age-group analysis.
    """

    result = (
        df.groupby(
            "Age_Group",
            observed=False
        )
        .agg(
            Students=("Student_ID", "count"),

            Avg_Attendance=(
                "Attendance_Percent",
                "mean"
            ),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            )
        )
        .reset_index()
    )

    return result.round(2)


def parent_education_analysis(df):
    """
    Parent education analysis.
    """

    result = (
        df.groupby("Parent_Education")
        .agg(
            Students=("Student_ID", "count"),

            Avg_Attendance=(
                "Attendance_Percent",
                "mean"
            ),

            Avg_Marks=(
                "Average_Marks",
                "mean"
            ),

            Avg_Study_Hours=(
                "Study_Hours",
                "mean"
            )
        )
        .reset_index()
    )

    return result.round(2)


def study_hours_correlation(df):
    """
    Calculate study hours and marks correlation.
    """

    return round(
        df[
            [
                "Study_Hours",
                "Average_Marks"
            ]
        ].corr().loc[
            "Study_Hours",
            "Average_Marks"
        ],
        3
    )


def academic_review(
    df,
    marks_threshold=50,
    attendance_threshold=75
):
    """
    Identify students requiring academic review.
    """

    result = df[
        (df["Average_Marks"] < marks_threshold)
        |
        (
            df["Attendance_Percent"]
            < attendance_threshold
        )
    ].copy()

    columns = [
        "Student_ID",
        "Class",
        "Section",
        "Attendance_Percent",
        "Average_Marks",
        "Performance_Band"
    ]

    return result[
        columns
    ].sort_values(
        "Average_Marks"
    )


def correlation_matrix(df):
    """
    Generate correlation matrix.
    """

    numeric_columns = [
        "Attendance_Percent",
        "Average_Marks",
        "Age",
        "Study_Hours"
    ]

    return df[
        numeric_columns
    ].corr().round(2)