# ============================================================
# DATA VISUALIZATION
# ============================================================

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from config import PLOTS_DIR

os.makedirs(PLOTS_DIR, exist_ok=True)

def subject_performance_chart(subject_summary):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=subject_summary, x="Subject", y="Average")
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "subject_performance.png"))
    plt.close()

def attendance_marks_scatter(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Attendance_Percent", y="Average_Marks")
    sns.regplot(data=df, x="Attendance_Percent", y="Average_Marks", scatter=False)
    plt.title("Attendance vs Average Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "attendance_marks_scatter.png"))
    plt.close()

def class_performance_chart(class_summary):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=class_summary, x="Class", y="Avg_Marks")
    plt.title("Average Marks by Class")
    plt.xlabel("Class")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "class_performance.png"))
    plt.close()

def class_subject_heatmap(class_subject):
    data = class_subject.set_index("Class")
    plt.figure(figsize=(10, 7))
    sns.heatmap(data, annot=True, fmt=".1f")
    plt.title("Class-Wise Subject Performance")
    plt.xlabel("Subject")
    plt.ylabel("Class")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "class_subject_heatmap.png"))
    plt.close()

def attendance_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Attendance_Percent"], bins=15, kde=True)
    plt.title("Distribution of Attendance")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "attendance_distribution.png"))
    plt.close()

def marks_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Average_Marks"], bins=15, kde=True)
    plt.title("Distribution of Average Marks")
    plt.xlabel("Average Marks")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "marks_distribution.png"))
    plt.close()

def performance_band_chart(df):
    counts = df["Performance_Band"].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Performance Band Distribution")
    plt.xlabel("Performance Band")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "performance_band_chart.png"))
    plt.close()

def attendance_band_chart(attendance_summary):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=attendance_summary, x="Attendance_Band", y="Avg_Marks")
    plt.title("Average Marks by Attendance Band")
    plt.xlabel("Attendance Band")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "attendance_band_chart.png"))
    plt.close()

def correlation_heatmap(correlation_data):
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_data, annot=True, fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"))
    plt.close()

def student_heatmap(df, subject_columns):
    data = df.set_index("Student_ID")[subject_columns].head(30)
    plt.figure(figsize=(11, 10))
    sns.heatmap(data, annot=True, fmt=".0f")
    plt.title("Student Subject Performance Heatmap")
    plt.xlabel("Subject")
    plt.ylabel("Student")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "student_heatmap.png"))
    plt.close()
