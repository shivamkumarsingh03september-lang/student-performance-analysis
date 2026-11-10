# ============================================================
# MAIN PROGRAM
# STUDENT PERFORMANCE & ATTENDANCE ANALYSIS
# ============================================================

import os

from config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    OUTPUT_DIR,
    SUBJECT_COLUMNS,
    UNDERPERFORMANCE_THRESHOLD,
    ATTENDANCE_THRESHOLD,
    MARKS_THRESHOLD
)

from src.data_loader import (
    load_data,
    inspect_data
)

from src.preprocessing import (
    clean_data,
    create_average_marks,
    create_performance_band,
    create_attendance_band,
    create_age_group
)

from src.analysis import (
    overall_performance,
    performance_band_analysis,
    attendance_analysis,
    attendance_marks_correlation,
    subject_analysis,
    underperforming_subjects,
    class_analysis,
    section_analysis,
    class_subject_analysis,
    attendance_band_analysis,
    gender_analysis,
    age_analysis,
    parent_education_analysis,
    study_hours_correlation,
    academic_review,
    correlation_matrix
)

from src.visualization import (
    subject_performance_chart,
    attendance_marks_scatter,
    class_performance_chart,
    class_subject_heatmap,
    attendance_distribution,
    marks_distribution,
    performance_band_chart,
    attendance_band_chart,
    correlation_heatmap,
    student_heatmap
)

from src.utils import (
    create_output_folder,
    save_dataframe,
    print_section
)


# ============================================================
# 1. CREATE OUTPUT FOLDER
# ============================================================

create_output_folder(OUTPUT_DIR)


# ============================================================
# 2. LOAD DATA
# ============================================================

print_section("1. LOAD DATA")

df = load_data(
    RAW_DATA_PATH
)

print(
    "Dataset loaded successfully."
)

print(
    "Rows:",
    df.shape[0]
)

print(
    "Columns:",
    df.shape[1]
)


# ============================================================
# 3. INSPECT DATA
# ============================================================

print_section("2. DATA INSPECTION")

inspect_data(df)


# ============================================================
# 4. DATA CLEANING
# ============================================================

print_section("3. DATA CLEANING")

df = clean_data(
    df,
    SUBJECT_COLUMNS
)

print(
    "Cleaned dataset shape:",
    df.shape
)


# ============================================================
# 5. CREATE DERIVED COLUMNS
# ============================================================

print_section("4. FEATURE CREATION")

df = create_average_marks(
    df,
    SUBJECT_COLUMNS
)

df = create_performance_band(
    df
)

df = create_attendance_band(
    df
)

df = create_age_group(
    df
)

print(
    "Average marks, performance bands,",
    "attendance bands and age groups created."
)


# ============================================================
# 6. OVERALL PERFORMANCE
# ============================================================

print_section("5. OVERALL PERFORMANCE")

overall = overall_performance(
    df
)

for key, value in overall.items():

    print(
        f"{key}: {value}"
    )


# ============================================================
# 7. PERFORMANCE BANDS
# ============================================================

print_section("6. PERFORMANCE BANDS")

performance_bands = (
    performance_band_analysis(df)
)

print(
    performance_bands
)


# ============================================================
# 8. ATTENDANCE ANALYSIS
# ============================================================

print_section("7. ATTENDANCE ANALYSIS")

attendance = attendance_analysis(
    df
)

for key, value in attendance.items():

    print(
        f"{key}: {value}"
    )


# ============================================================
# 9. ATTENDANCE VS MARKS
# ============================================================

print_section(
    "8. ATTENDANCE VS MARKS CORRELATION"
)

attendance_corr = (
    attendance_marks_correlation(df)
)

print(
    "Correlation:",
    attendance_corr
)


# ============================================================
# 10. SUBJECT ANALYSIS
# ============================================================

print_section(
    "9. SUBJECT-WISE ANALYSIS"
)

subject_summary = subject_analysis(
    df,
    SUBJECT_COLUMNS
)

print(
    subject_summary
)


# ============================================================
# 11. UNDERPERFORMING SUBJECTS
# ============================================================

print_section(
    "10. UNDERPERFORMING SUBJECTS"
)

weak_subjects = underperforming_subjects(
    subject_summary,
    UNDERPERFORMANCE_THRESHOLD
)

if weak_subjects.empty:

    print(
        "No subject is below the threshold."
    )

else:

    print(
        weak_subjects
    )


# ============================================================
# 12. CLASS ANALYSIS
# ============================================================

print_section(
    "11. CLASS-WISE ANALYSIS"
)

class_summary = class_analysis(
    df
)

print(
    class_summary
)


# ============================================================
# 13. SECTION ANALYSIS
# ============================================================

print_section(
    "12. SECTION-WISE ANALYSIS"
)

section_summary = section_analysis(
    df
)

print(
    section_summary
)


# ============================================================
# 14. CLASS SUBJECT ANALYSIS
# ============================================================

print_section(
    "13. CLASS-WISE SUBJECT ANALYSIS"
)

class_subject = class_subject_analysis(
    df,
    SUBJECT_COLUMNS
)

print(
    class_subject
)


# ============================================================
# 15. ATTENDANCE BAND ANALYSIS
# ============================================================

print_section(
    "14. ATTENDANCE BAND ANALYSIS"
)

attendance_summary = (
    attendance_band_analysis(df)
)

print(
    attendance_summary
)


# ============================================================
# 16. GENDER ANALYSIS
# ============================================================

print_section(
    "15. GENDER ANALYSIS"
)

gender_summary = gender_analysis(
    df
)

print(
    gender_summary
)


# ============================================================
# 17. AGE ANALYSIS
# ============================================================

print_section(
    "16. AGE GROUP ANALYSIS"
)

age_summary = age_analysis(
    df
)

print(
    age_summary
)


# ============================================================
# 18. PARENT EDUCATION
# ============================================================

print_section(
    "17. PARENT EDUCATION ANALYSIS"
)

parent_summary = (
    parent_education_analysis(df)
)

print(
    parent_summary
)


# ============================================================
# 19. STUDY HOURS
# ============================================================

print_section(
    "18. STUDY HOURS VS MARKS"
)

study_corr = study_hours_correlation(
    df
)

print(
    "Study Hours vs Marks Correlation:",
    study_corr
)


# ============================================================
# 20. ACADEMIC REVIEW
# ============================================================

print_section(
    "19. STUDENTS REQUIRING ACADEMIC REVIEW"
)

review_students = academic_review(
    df,
    MARKS_THRESHOLD,
    ATTENDANCE_THRESHOLD
)

print(
    "Students requiring review:",
    len(review_students)
)

print(
    review_students.head(20)
)


# ============================================================
# 21. CORRELATION MATRIX
# ============================================================

print_section(
    "20. CORRELATION MATRIX"
)

corr_matrix = correlation_matrix(
    df
)

print(
    corr_matrix
)


# ============================================================
# 22. SAVE PROCESSED DATA
# ============================================================

print_section(
    "21. SAVING OUTPUT FILES"
)

os.makedirs(
    os.path.dirname(PROCESSED_DATA_PATH),
    exist_ok=True
)

df.to_csv(
    PROCESSED_DATA_PATH,
    index=False
)

print(
    "Processed data saved:"
)

print(
    PROCESSED_DATA_PATH
)


# ============================================================
# 23. SAVE ANALYSIS REPORTS
# ============================================================

save_dataframe(
    subject_summary,
    "subject_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    class_summary,
    "class_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    section_summary,
    "section_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    class_subject,
    "class_subject_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    attendance_summary,
    "attendance_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    gender_summary,
    "gender_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    age_summary,
    "age_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    parent_summary,
    "parent_education_summary.csv",
    OUTPUT_DIR
)

save_dataframe(
    review_students,
    "academic_review_students.csv",
    OUTPUT_DIR
)


# ============================================================
# 24. CREATE VISUALIZATIONS
# ============================================================

print_section(
    "22. CREATING VISUALIZATIONS"
)

subject_performance_chart(
    subject_summary
)

attendance_marks_scatter(
    df
)

class_performance_chart(
    class_summary
)

class_subject_heatmap(
    class_subject
)

attendance_distribution(
    df
)

marks_distribution(
    df
)

performance_band_chart(
    df
)

attendance_band_chart(
    attendance_summary
)

correlation_heatmap(
    corr_matrix
)

student_heatmap(
    df,
    SUBJECT_COLUMNS
)


# ============================================================
# 25. FINAL SUMMARY
# ============================================================

print_section(
    "FINAL DATA ANALYTICS SUMMARY"
)

print(
    "Total Students:",
    len(df)
)

print(
    "Overall Average Marks:",
    round(
        df["Average_Marks"].mean(),
        2
    )
)

print(
    "Average Attendance:",
    round(
        df["Attendance_Percent"].mean(),
        2
    )
)

best_subject = subject_summary.loc[
    subject_summary["Average"].idxmax()
]

weakest_subject = subject_summary.loc[
    subject_summary["Average"].idxmin()
]

print(
    "\nHighest Performing Subject:",
    best_subject["Subject"],
    "-",
    best_subject["Average"]
)

print(
    "Lowest Performing Subject:",
    weakest_subject["Subject"],
    "-",
    weakest_subject["Average"]
)

best_class = class_summary.loc[
    class_summary["Avg_Marks"].idxmax()
]

lowest_class = class_summary.loc[
    class_summary["Avg_Marks"].idxmin()
]

print(
    "\nBest Performing Class:",
    best_class["Class"],
    "-",
    best_class["Avg_Marks"]
)

print(
    "Lowest Performing Class:",
    lowest_class["Class"],
    "-",
    lowest_class["Avg_Marks"]
)

print(
    "\nAttendance vs Marks Correlation:",
    attendance_corr
)

print(
    "Students Requiring Review:",
    len(review_students)
)

print(
    "\n========== ANALYSIS COMPLETED =========="
)