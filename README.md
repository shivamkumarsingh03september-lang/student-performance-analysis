# 🎓 Student Performance & Attendance Analytics Dashboard


---

## 📋 Project Overview

The **Student Performance & Attendance Analytics Dashboard** is an interactive, data-driven web application designed to evaluate student academic performance, track attendance records, analyze subject-wise distributions, and flag at-risk students in real time. 

Built using **Python** and **Streamlit**, the application provides educators and administrators with actionable insights through dynamic dataset uploads, custom filtering, and visual analytics.

---

## ✨ Key Features

1. **Functional Streamlit Frontend**: Fully interactive, web-based dashboard user interface.
2. **Dynamic Dataset Upload**: Supports direct CSV dataset uploads via the sidebar uploader for real-time processing and dynamic analysis.
3. **Interactive Cohort Filtering**: Filter data dynamically across Class, Section, Gender, Performance Bands, and Attendance Bands.
4. **Automated At-Risk Detection**: Real-time identification and filtering of students below customizable grade and attendance thresholds.
5. **Multi-Tab Visual Analytics**:
   - **📊 Overview**: High-level KPIs, attendance vs. marks scatter plots, and correlation metrics.
   - **📚 Subjects**: Strongest/weakest subject highlights, score box plots, and inter-subject correlation heatmaps.
   - **⚖️ Compare Groups**: Dynamic group-by aggregations and summary data tables.
   - **🚨 At Risk**: Flagged student rosters with instant CSV export capabilities.
   - **🧑‍🎓 Student Profile**: Deep-dive profile comparisons pitting individual performance against cohort averages.
   - **🗂️ Records**: Searchable dataset view with built-in progress bar metrics.

---

## 🛠️ Technologies & Libraries Used

- **Programming Language**: Python 3.10+
- **Frontend Web Framework**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Altair, Matplotlib, Seaborn

---

## 📁 Project Structure

```text
student_performance_analysis/
├── app.py                  # Streamlit web application dashboard (Frontend)
├── main.py                 # Core CLI execution script & offline reporting pipeline
├── config.py               # Project paths and configuration settings
├── requirements.txt        # Python package dependencies
├── README.md               # Project documentation
├── data/
│   ├── raw/                # Raw input datasets (student_performance.csv)
│   └── processed/          # Cleaned and engineered output datasets
├── src/                    # Source code modules
│   ├── analysis.py         # Statistical analysis logic
│   ├── data_loader.py      # Data ingestion pipelines
│   ├── preprocessing.py   # Data cleaning, feature engineering, and categorization
│   ├── utils.py            # Helper functions
│   └── visualization.py    # Chart generation modules
└── outputs/                # Generated CSV summary reports and static charts
🚀 Getting Started
1. Prerequisites & Installation
Clone the repository and install the required dependencies:

# Navigate to the project directory
cd student-performance-analysis

# Install required Python packages
pip install -r requirements.txt
2. Running the Interactive Streamlit Web Application
Launch the Streamlit dashboard in your local browser:

Bash
streamlit run app.py
3. Running the Offline Analysis Pipeline (Optional)
Execute the CLI pipeline to generate summary CSV outputs in the outputs/ folder:

Bash
python main.py
📊 Summary of Analysis & Outputs
The application automatically processes raw student records to generate:

Cleaned datasets with normalized performance and attendance bands.

Subject-wise statistical summaries (mean, min, max, score distributions).

Demographic summaries (Class, Section, Gender, Parent Education breakdowns).

At-risk student registers exported directly for academic review.

🔗 Repository Access
GitHub Repository URL: https://github.com/shivamkumarsingh03september-lang/student-performance-analysis.git
