# ============================================================
# CONFIGURATION FILE
# ============================================================

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "student_performance.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_student_performance.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"

SUBJECT_COLUMNS = [
    "Maths",
    "Science",
    "English",
    "Social_Science",
    "Computer"
]

UNDERPERFORMANCE_THRESHOLD = 50
ATTENDANCE_THRESHOLD = 75
MARKS_THRESHOLD = 50
