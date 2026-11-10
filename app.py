import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from io import BytesIO

from config import RAW_DATA_PATH, SUBJECT_COLUMNS
from src.data_loader import load_data
from src.preprocessing import (
    clean_data,
    create_average_marks,
    create_performance_band,
    create_attendance_band,
    create_age_group,
)

# ----------------------------------------------------------------------------
# Page setup & styling
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
    }
    div[data-testid="stMetricLabel"] {font-weight: 600; opacity: 0.8;}
    button[data-baseweb="tab"] {font-size: 1rem; font-weight: 600;}
    </style>
    """,
    unsafe_allow_html=True,
)

PALETTE = "tealblues"
ID_CANDIDATES = ["Student_ID", "StudentID", "Student_Id", "ID", "Roll_No", "Roll", "RollNo"]
NAME_CANDIDATES = ["Name", "Student_Name", "StudentName", "Full_Name"]
GROUP_CANDIDATES = ["Class", "Section", "Gender", "Age_Group", "Performance_Band", "Attendance_Band"]


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def stretch(fn, *args, **kwargs):
    """Call a Streamlit element full-width on both old and new Streamlit versions."""
    try:
        return fn(*args, width="stretch", **kwargs)
    except TypeError:
        return fn(*args, use_container_width=True, **kwargs)


@st.cache_data(show_spinner="Processing data...")
def process_data(file_path, uploaded_bytes=None):
    if uploaded_bytes is not None:
        df = pd.read_csv(BytesIO(uploaded_bytes))
    else:
        df = load_data(file_path)

    df = clean_data(df, SUBJECT_COLUMNS)
    df = create_average_marks(df, SUBJECT_COLUMNS)
    df = create_performance_band(df)
    df = create_attendance_band(df)
    df = create_age_group(df)
    return df


def first_present(columns, candidates):
    return next((c for c in candidates if c in columns), None)


def bar_chart(data, x, y, title=None, color=None, horizontal=False, fmt=".1f", height=320):
    """Clean Altair bar chart with value labels and tooltips."""
    x_enc = alt.X(x, sort="-y" if not horizontal else "-x", title=None)
    base = alt.Chart(data, height=height)
    if horizontal:
        bars = base.mark_bar(cornerRadiusEnd=4).encode(
            y=alt.Y(x, sort="-x", title=None),
            x=alt.X(y, title=None),
            color=alt.Color(y, scale=alt.Scale(scheme=PALETTE), legend=None) if color is None else alt.Color(color),
            tooltip=[x, alt.Tooltip(y, format=fmt)],
        )
        labels = base.mark_text(align="left", dx=4).encode(
            y=alt.Y(x, sort="-x"), x=alt.X(y), text=alt.Text(y, format=fmt)
        )
    else:
        bars = base.mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=x_enc,
            y=alt.Y(y, title=None),
            color=alt.Color(y, scale=alt.Scale(scheme=PALETTE), legend=None) if color is None else alt.Color(color),
            tooltip=[x, alt.Tooltip(y, format=fmt)],
        )
        labels = base.mark_text(dy=-8).encode(x=alt.X(x, sort="-y"), y=alt.Y(y), text=alt.Text(y, format=fmt))
    chart = bars + labels
    if title:
        chart = chart.properties(title=title)
    stretch(st.altair_chart, chart)


def counts_frame(series, name):
    out = series.value_counts().rename_axis(name).reset_index(name="Students")
    return out


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("🎓 Student Performance Analytics Dashboard")
st.caption("Explore marks, attendance and risk signals. Use the sidebar to filter and tune thresholds.")

# ----------------------------------------------------------------------------
# Sidebar: data source
# ----------------------------------------------------------------------------
st.sidebar.header("⚙️ Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload a student CSV (optional)",
    type=["csv"],
    help="If you don't upload anything, the default dataset is used.",
)

try:
    if uploaded_file is not None:
        df = process_data(str(RAW_DATA_PATH), uploaded_file.getvalue())
    else:
        df = process_data(str(RAW_DATA_PATH))

    st.sidebar.success(f"{len(df):,} records loaded")

    # ------------------------------------------------------------------------
    # Sidebar: filters
    # ------------------------------------------------------------------------
    st.sidebar.subheader("🔎 Filters")

    filter_specs = [
        ("Class", "Class"),
        ("Section", "Section"),
        ("Gender", "Gender"),
        ("Performance_Band", "Performance Band"),
        ("Attendance_Band", "Attendance Band"),
    ]
    active_filters = [(c, l) for c, l in filter_specs if c in df.columns]

    def reset_filters():
        for col, _ in active_filters:
            st.session_state[f"filter_{col}"] = sorted(df[col].dropna().unique().tolist(), key=str)

    st.sidebar.button("↺ Reset filters", on_click=reset_filters)

    mask = pd.Series(True, index=df.index)
    for col, label in active_filters:
        options = sorted(df[col].dropna().unique().tolist(), key=str)
        selected = st.sidebar.multiselect(label, options, default=options, key=f"filter_{col}")
        mask &= df[col].isin(selected)
    filtered = df[mask].copy()

    # ------------------------------------------------------------------------
    # Sidebar: thresholds
    # ------------------------------------------------------------------------
    st.sidebar.subheader("🎚️ Thresholds")
    pass_mark = st.sidebar.slider("Pass mark (avg)", 0, 100, 40)
    risk_marks = st.sidebar.slider("At-risk: marks below", 0, 100, 50)
    risk_att = st.sidebar.slider("At-risk: attendance below (%)", 0, 100, 75)

    has_marks = "Average_Marks" in filtered.columns
    has_att = "Attendance_Percent" in filtered.columns

    if filtered.empty:
        st.warning("No students match these filters. Try resetting them from the sidebar.")
        st.stop()

    # ------------------------------------------------------------------------
    # At-risk flag (computed once, reused by several tabs)
    # ------------------------------------------------------------------------
    low_marks = (filtered["Average_Marks"] < risk_marks) if has_marks else pd.Series(False, index=filtered.index)
    low_att = (filtered["Attendance_Percent"] < risk_att) if has_att else pd.Series(False, index=filtered.index)
    filtered["Risk_Reason"] = np.select(
        [low_marks & low_att, low_marks, low_att],
        ["Low marks + low attendance", "Low marks", "Low attendance"],
        default="",
    )
    at_risk = filtered[filtered["Risk_Reason"] != ""]

    # ------------------------------------------------------------------------
    # KPI row
    # ------------------------------------------------------------------------
    total = len(filtered)
    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total Students", f"{total:,}", delta=f"{total / len(df):.0%} of all", delta_color="off")

    if has_marks:
        avg_m = filtered["Average_Marks"].mean()
        k2.metric("Average Marks", f"{avg_m:.1f}", delta=f"{avg_m - df['Average_Marks'].mean():+.1f} vs all")
        pass_rate = (filtered["Average_Marks"] >= pass_mark).mean() * 100
        k3.metric("Pass Rate", f"{pass_rate:.1f}%")
    else:
        k2.metric("Average Marks", "N/A")
        k3.metric("Pass Rate", "N/A")

    if has_att:
        avg_a = filtered["Attendance_Percent"].mean()
        k4.metric("Average Attendance", f"{avg_a:.1f}%", delta=f"{avg_a - df['Attendance_Percent'].mean():+.1f} vs all")
    else:
        k4.metric("Average Attendance", "N/A")

    k5.metric(
        "Students at Risk",
        f"{len(at_risk):,}",
        delta=f"{len(at_risk) / total:.0%} of selection",
        delta_color="inverse",
    )

    st.write("")

    # ------------------------------------------------------------------------
    # Tabs
    # ------------------------------------------------------------------------
    tab_overview, tab_subjects, tab_compare, tab_risk, tab_profile, tab_records = st.tabs(
        ["📊 Overview", "📚 Subjects", "⚖️ Compare Groups", "🚨 At Risk", "🧑‍🎓 Student Profile", "🗂️ Records"]
    )

    # ---- Overview ----------------------------------------------------------
    with tab_overview:
        left, right = st.columns(2)

        with left:
            st.subheader("Performance Distribution")
            if "Performance_Band" in filtered.columns:
                bar_chart(counts_frame(filtered["Performance_Band"], "Band"), "Band", "Students", fmt=",d")
            else:
                st.info("Performance band not available.")

        with right:
            st.subheader("Attendance Distribution")
            if has_att:
                bins = pd.cut(
                    filtered["Attendance_Percent"],
                    bins=[-float("inf"), 50, 60, 75, 90, float("inf")],
                    labels=["≤50%", "51–60%", "61–75%", "76–90%", ">90%"],
                )
                att_df = bins.value_counts().sort_index().rename_axis("Attendance").reset_index(name="Students")
                chart = (
                    alt.Chart(att_df, height=320)
                    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                    .encode(
                        x=alt.X("Attendance:N", sort=list(att_df["Attendance"]), title=None),
                        y=alt.Y("Students:Q", title=None),
                        color=alt.Color("Students:Q", scale=alt.Scale(scheme=PALETTE), legend=None),
                        tooltip=["Attendance", "Students"],
                    )
                )
                labels = chart.mark_text(dy=-8).encode(text="Students:Q")
                stretch(st.altair_chart, chart + labels)
            else:
                st.info("Attendance data not available.")

        st.subheader("Attendance vs Marks")
        if has_att and has_marks:
            sc = filtered.dropna(subset=["Attendance_Percent", "Average_Marks"])
            tooltip_cols = [c for c in [first_present(sc.columns, NAME_CANDIDATES), first_present(sc.columns, ID_CANDIDATES),
                                         "Attendance_Percent", "Average_Marks"] if c]
            color_enc = (
                alt.Color("Performance_Band:N", title="Band")
                if "Performance_Band" in sc.columns
                else alt.value("#1f77b4")
            )
            points = (
                alt.Chart(sc, height=380)
                .mark_circle(size=70, opacity=0.65)
                .encode(
                    x=alt.X("Attendance_Percent:Q", title="Attendance %", scale=alt.Scale(zero=False)),
                    y=alt.Y("Average_Marks:Q", title="Average marks", scale=alt.Scale(zero=False)),
                    color=color_enc,
                    tooltip=tooltip_cols,
                )
            )
            trend = (
                alt.Chart(sc)
                .transform_regression("Attendance_Percent", "Average_Marks")
                .mark_line(color="#e45756", strokeDash=[6, 4], size=2)
                .encode(x="Attendance_Percent:Q", y="Average_Marks:Q")
            )
            stretch(st.altair_chart, (points + trend).interactive())
            if len(sc) > 2:
                corr = sc["Attendance_Percent"].corr(sc["Average_Marks"])
                st.caption(f"Correlation between attendance and marks: **{corr:.2f}** (dashed line = trend).")
        else:
            st.info("Need both attendance and average marks to draw this chart.")

    # ---- Subjects ----------------------------------------------------------
    with tab_subjects:
        subjects = [c for c in SUBJECT_COLUMNS if c in filtered.columns and pd.api.types.is_numeric_dtype(filtered[c])]
        if not subjects:
            st.info("No numeric subject columns found.")
        else:
            chosen = st.multiselect("Choose subjects", subjects, default=subjects)
            if chosen:
                subj_avg = filtered[chosen].mean().rename_axis("Subject").reset_index(name="Average Marks")
                best = subj_avg.loc[subj_avg["Average Marks"].idxmax()]
                worst = subj_avg.loc[subj_avg["Average Marks"].idxmin()]

                m1, m2 = st.columns(2)
                m1.metric("💪 Strongest subject", best["Subject"], f"{best['Average Marks']:.1f} avg")
                m2.metric("⚠️ Weakest subject", worst["Subject"], f"{worst['Average Marks']:.1f} avg", delta_color="inverse")

                c_left, c_right = st.columns(2)
                with c_left:
                    st.subheader("Average by Subject")
                    bar_chart(subj_avg, "Subject", "Average Marks")
                with c_right:
                    st.subheader("Score Spread")
                    long = filtered[chosen].melt(var_name="Subject", value_name="Marks").dropna()
                    box = (
                        alt.Chart(long, height=320)
                        .mark_boxplot(extent="min-max", size=36)
                        .encode(
                            x=alt.X("Subject:N", title=None),
                            y=alt.Y("Marks:Q", title=None),
                            color=alt.Color("Subject:N", legend=None, scale=alt.Scale(scheme="tableau10")),
                        )
                    )
                    stretch(st.altair_chart, box)

                if len(chosen) > 1:
                    st.subheader("Subject Correlation")
                    corr = filtered[chosen].corr().round(2).reset_index().melt("index")
                    corr.columns = ["A", "B", "Correlation"]
                    heat = alt.Chart(corr, height=340).mark_rect().encode(
                        x=alt.X("A:N", title=None), y=alt.Y("B:N", title=None),
                        color=alt.Color("Correlation:Q", scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 1])),
                        tooltip=["A", "B", "Correlation"],
                    )
                    txt = heat.mark_text(baseline="middle").encode(text=alt.Text("Correlation:Q", format=".2f"), color=alt.value("black"))
                    stretch(st.altair_chart, heat + txt)
                    st.caption("Higher values mean students who do well in one subject tend to do well in the other.")

    # ---- Compare groups ----------------------------------------------------
    with tab_compare:
        group_cols = [c for c in GROUP_CANDIDATES if c in filtered.columns]
        if not group_cols:
            st.info("No grouping columns (Class, Section, Gender...) found.")
        else:
            group_by = st.selectbox("Compare by", group_cols)
            agg = {"Students": (group_by, "size")}
            if has_marks:
                agg["Avg Marks"] = ("Average_Marks", "mean")
            if has_att:
                agg["Avg Attendance"] = ("Attendance_Percent", "mean")
            grouped = filtered.groupby(group_by, dropna=False).agg(**agg).reset_index()
            grouped[group_by] = grouped[group_by].astype(str)

            c_left, c_right = st.columns(2)
            if has_marks:
                with c_left:
                    st.subheader("Average Marks")
                    bar_chart(grouped, group_by, "Avg Marks")
            if has_att:
                with c_right:
                    st.subheader("Average Attendance (%)")
                    bar_chart(grouped, group_by, "Avg Attendance")

            st.subheader("Summary Table")
            stretch(st.dataframe, grouped.round(2), hide_index=True)

    # ---- At risk -----------------------------------------------------------
    with tab_risk:
        st.subheader("Students Needing Attention")
        st.caption(f"Flagged when average marks < {risk_marks} or attendance < {risk_att}%. Change this in the sidebar.")

        if at_risk.empty:
            st.success("🎉 No students are flagged with the current thresholds.")
        else:
            r1, r2, r3 = st.columns(3)
            r1.metric("Low marks + attendance", int((at_risk["Risk_Reason"] == "Low marks + low attendance").sum()))
            r2.metric("Low marks only", int((at_risk["Risk_Reason"] == "Low marks").sum()))
            r3.metric("Low attendance only", int((at_risk["Risk_Reason"] == "Low attendance").sum()))

            sort_col = "Average_Marks" if has_marks else at_risk.columns[0]
            risk_view = at_risk.sort_values(sort_col)
            lead = [c for c in [first_present(risk_view.columns, ID_CANDIDATES), first_present(risk_view.columns, NAME_CANDIDATES),
                                "Class", "Section", "Average_Marks", "Attendance_Percent", "Risk_Reason"] if c and c in risk_view.columns]
            stretch(st.dataframe, risk_view[lead], hide_index=True)

            st.download_button(
                "⬇️ Download at-risk list",
                data=risk_view.to_csv(index=False).encode("utf-8"),
                file_name="students_at_risk.csv",
                mime="text/csv",
            )

    # ---- Student profile ---------------------------------------------------
    with tab_profile:
        id_col = first_present(filtered.columns, ID_CANDIDATES)
        name_col = first_present(filtered.columns, NAME_CANDIDATES)

        if id_col and name_col:
            labels = filtered[id_col].astype(str) + " · " + filtered[name_col].astype(str)
        elif id_col or name_col:
            labels = filtered[id_col or name_col].astype(str)
        else:
            labels = pd.Series([f"Row {i}" for i in filtered.index], index=filtered.index)

        pick = st.selectbox("Select a student", labels.tolist())
        student = filtered.loc[labels[labels == pick].index[0]]

        p1, p2, p3 = st.columns(3)
        if has_marks:
            p1.metric("Average Marks", f"{student['Average_Marks']:.1f}",
                      delta=f"{student['Average_Marks'] - filtered['Average_Marks'].mean():+.1f} vs cohort")
        if has_att:
            p2.metric("Attendance", f"{student['Attendance_Percent']:.1f}%",
                      delta=f"{student['Attendance_Percent'] - filtered['Attendance_Percent'].mean():+.1f} vs cohort")
        if "Performance_Band" in filtered.columns:
            p3.metric("Performance Band", str(student["Performance_Band"]))

        if student["Risk_Reason"]:
            st.warning(f"Flagged: {student['Risk_Reason']}")

        subjects = [c for c in SUBJECT_COLUMNS if c in filtered.columns and pd.api.types.is_numeric_dtype(filtered[c])]
        if subjects:
            comp = pd.DataFrame({
                "Subject": subjects * 2,
                "Marks": [student[s] for s in subjects] + [filtered[s].mean() for s in subjects],
                "Who": ["Student"] * len(subjects) + ["Cohort average"] * len(subjects),
            })
            chart = (
                alt.Chart(comp, height=340)
                .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                .encode(
                    x=alt.X("Subject:N", title=None),
                    xOffset="Who:N",
                    y=alt.Y("Marks:Q", title=None),
                    color=alt.Color("Who:N", title=None, scale=alt.Scale(range=["#9ecae1", "#08519c"][::-1])),
                    tooltip=["Subject", "Who", alt.Tooltip("Marks:Q", format=".1f")],
                )
            )
            stretch(st.altair_chart, chart)

    # ---- Records -----------------------------------------------------------
    with tab_records:
        st.subheader("Student Records")
        s_col, c_col = st.columns([2, 3])
        search = s_col.text_input("Search", placeholder="Type a student name or ID...")
        shown_cols = c_col.multiselect("Columns", filtered.columns.tolist(), default=filtered.columns.tolist())

        display_df = filtered[shown_cols] if shown_cols else filtered
        if search:
            m = display_df.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False, regex=False)
            ).any(axis=1)
            display_df = display_df[m]

        col_cfg = {}
        if "Average_Marks" in display_df.columns:
            col_cfg["Average_Marks"] = st.column_config.ProgressColumn(
                "Average Marks", min_value=0, max_value=100, format="%.1f")
        if "Attendance_Percent" in display_df.columns:
            col_cfg["Attendance_Percent"] = st.column_config.ProgressColumn(
                "Attendance %", min_value=0, max_value=100, format="%.1f")

        st.caption(f"Showing {len(display_df):,} of {len(df):,} records")
        stretch(st.dataframe, display_df, hide_index=True, column_config=col_cfg)

        st.download_button(
            "⬇️ Download filtered CSV",
            data=display_df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_student_performance.csv",
            mime="text/csv",
        )

except Exception as e:
    st.error("Dashboard could not be loaded.")
    st.exception(e)