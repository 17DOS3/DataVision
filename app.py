
# ============================================
# DATAVISION - DATA ANALYTICS PLATFORM
# ============================================

# ============================================
# IMPORTS
# ============================================

from io import BytesIO
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
# ============================================
# 1. PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="DataVision",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# 2. CUSTOM CSS - DESIGN SYSTEM
# ============================================

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background-color: #F8FAFC;
    color: #1E293B;
    font-family: "Inter", sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* HEADINGS */
h1, h2, h3 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

p, label {
    color: #475569;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 9px;
    padding: 9px 12px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #EFF6FF;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background-color: #DBEAFE;
    color: #1D4ED8;
    font-weight: 700;
}

/* SIDEBAR BRAND */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 4px 24px 4px;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 24px;
}

.brand-icon {
    background: #EFF6FF;
    color: #2563EB;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
}

.sidebar-brand h2 {
    font-size: 19px;
    margin: 0;
    color: #0F172A;
}

.sidebar-brand p {
    font-size: 11px;
    margin: 3px 0 0 0;
    color: #64748B;
}

.sidebar-section {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 22px 20px;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #93C5FD;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.09);
    transform: translateY(-3px);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #1D4ED8 !important;
    font-size: 28px !important;
    font-weight: 750 !important;
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 9px;
    padding: 9px 18px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #1D4ED8;
    color: #FFFFFF;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #1E293B;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 1px dashed #93C5FD;
    border-radius: 12px;
    padding: 12px;
}

/* DIVIDER */
hr {
    border-color: #E2E8F0;
}

/* =================================
   DATAVISION - FINAL UI POLISH
================================= */

/* Main application */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Page titles */
h1, h2, h3 {
    color: #0F172A;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Paragraphs and captions */
.stCaption, small {
    color: #64748B;
}

/* KPI Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #0F172A;
    font-weight: 700;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #2563EB;
    color: #2563EB;
    transform: translateY(-1px);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 9px;
}

/* Dataframes and tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    overflow: hidden;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px dashed #93C5FD;
    border-radius: 12px;
    padding: 12px;
}

/* Alerts and messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid #E2E8F0;
}

/* Dividers */
hr {
    border-color: #E2E8F0;
}

/* Responsive layout */
@media (max-width: 768px) {

    .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }

    h1 {
        font-size: 1.7rem;
    }

    h2 {
        font-size: 1.35rem;
    }

    [data-testid="stMetric"] {
        padding: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================
# 3. INITIALIZE SESSION STATE
# ============================================

if "df" not in st.session_state:
    st.session_state.df = None

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "source_name" not in st.session_state:
    st.session_state.source_name = None


# ============================================
# 4. HELPER FUNCTIONS
# ============================================

def style_chart(fig):
    """Apply the DataVision chart design."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            color="#1E293B",
            family="Inter"
        ),
        title_font=dict(
            color="#0F172A",
            size=18
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False
    )

    return fig


def load_dataset(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):

        try:
            return pd.read_csv(uploaded_file, encoding="utf-8")

        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin-1")

    elif file_name.endswith((".xlsx", ".xls")):

        return pd.read_excel(uploaded_file)

    return None


def create_pdf_report(dataframe):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()
    elements = []

    # COLORS
    primary = colors.HexColor("#2563EB")
    dark = colors.HexColor("#0F172A")
    light = colors.HexColor("#EFF6FF")

    # CUSTOM STYLES
    title_style = ParagraphStyle(
        "DataVisionTitle",
        parent=styles["Title"],
        textColor=primary,
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER,
        fontSize=10
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=dark,
        fontSize=14,
        spaceBefore=14,
        spaceAfter=8
    )

    # HEADER
    elements.append(
        Paragraph("DataVision", title_style)
    )

    elements.append(
        Paragraph(
            "DATA ANALYSIS & QUALITY REPORT",
            subtitle_style
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )

    # DATASET OVERVIEW
    elements.append(
        Paragraph("1. Dataset Overview", heading_style)
    )

    total_rows = dataframe.shape[0]
    total_columns = dataframe.shape[1]
    total_cells = dataframe.size

    missing_values = int(
        dataframe.isnull().sum().sum()
    )

    duplicates = int(
        dataframe.duplicated().sum()
    )

    completeness = (
        (total_cells - missing_values) / total_cells * 100
        if total_cells > 0 else 0
    )

    overview_data = [
        ["Metric", "Value"],
        ["Total Rows", f"{total_rows:,}"],
        ["Total Columns", total_columns],
        ["Missing Values", missing_values],
        ["Duplicate Rows", duplicates],
        ["Completeness", f"{completeness:.1f}%"]
    ]

    overview_table = Table(
        overview_data,
        colWidths=[90 * mm, 75 * mm]
    )

    overview_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, -1), light),
            ("TEXTCOLOR", (0, 1), (-1, -1), dark),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elements.append(overview_table)

        # VALIDITY ANALYSIS

    validation_results = []

    for col in dataframe.columns:

        col_name = str(col).lower()
        non_null = dataframe[col].dropna()

        # Email validation
        if "email" in col_name:

            invalid_count = int(
                (~non_null.astype(str).str.fullmatch(
                    r"[^@\s]+@[^@\s]+\.[^@\s]+"
                )).sum()
            )

            validation_results.append({
                "Column": col,
                "Validation Rule": "Valid email format",
                "Invalid Values": invalid_count,
                "Checked Values": len(non_null)
            })

        # Negative values in common non-negative fields
        elif any(
            word in col_name
            for word in [
                "age", "salary", "price",
                "amount", "revenue", "quantity", "income"
            ]
        ) and pd.api.types.is_numeric_dtype(dataframe[col]):

            invalid_count = int((non_null < 0).sum())

            validation_results.append({
                "Column": col,
                "Validation Rule": "No negative values",
                "Invalid Values": invalid_count,
                "Checked Values": len(non_null)
            })

    if validation_results:

        validation_df = pd.DataFrame(validation_results)

        total_checked = int(
            validation_df["Checked Values"].sum()
        )

        total_invalid = int(
            validation_df["Invalid Values"].sum()
        )

        validity = (
            (total_checked - total_invalid) / total_checked * 100
            if total_checked > 0 else None
        )

    else:
        validation_df = pd.DataFrame()
        validity = None

    # DATA QUALITY

    elements.append(
        Paragraph("2. Data Quality Analysis", heading_style)
    )

    whitespace_issues = 0

    for column in dataframe.select_dtypes(
        include=["object", "string"]
    ).columns:

        values = dataframe[column].dropna().astype(str)

        whitespace_issues += int(
            values.ne(values.str.strip()).sum()
        )

    consistency_issues = duplicates + whitespace_issues

    quality_data = [
        ["Quality Metric", "Result"],
        ["Completeness", f"{completeness:.1f}%"],
        ["Validity", f"{validity:.1f}%" if validity is not None else "N/A"],
        ["Missing Values", missing_values],
        ["Duplicate Rows", duplicates],
        ["Whitespace Issues", whitespace_issues],
        ["Total Consistency Issues", consistency_issues]
    ]

    quality_table = Table(
        quality_data,
        colWidths=[90 * mm, 75 * mm]
    )

    quality_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, -1), light),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elements.append(quality_table)

        # VALIDITY DETAILS TABLE

    elements.append(
        Spacer(1, 10)
    )

    elements.append(
        Paragraph(
            "Validity Details",
            heading_style
        )
    )

    if not validation_df.empty:

        validity_data = [
            [
                "Column",
                "Validation Rule",
                "Checked",
                "Invalid"
            ]
        ]

        for _, row in validation_df.iterrows():

            validity_data.append([
                str(row["Column"]),
                str(row["Validation Rule"]),
                int(row["Checked Values"]),
                int(row["Invalid Values"])
            ])

        validity_table = Table(
            validity_data,
            colWidths=[35 * mm, 65 * mm, 35 * mm, 35 * mm],
            repeatRows=1
        )

        validity_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
            ])
        )

        elements.append(validity_table)

    else:

        elements.append(
            Paragraph(
                "No automatic validation rules were applicable.",
                styles["Normal"]
            )
        )

        # MISSING VALUES DATA

    missing_by_column = dataframe.isnull().sum()

    missing_by_column = missing_by_column[
        missing_by_column > 0
    ]
    # MISSING VALUES CHART
    
    if not missing_by_column.empty:
    
        fig, ax = plt.subplots(figsize=(8, 3.5))

        missing_by_column.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_title("Missing Values by Column")
        ax.set_xlabel("Number of Missing Values")
        ax.set_ylabel("Columns")

        fig.tight_layout()

        chart_buffer = BytesIO()

        fig.savefig(
            chart_buffer,
            format="png",
            dpi=150,
            bbox_inches="tight"
        )

        plt.close(fig)

        chart_buffer.seek(0)

        elements.append(
            Spacer(1, 10)
        )

        elements.append(
            Image(
                chart_buffer,
                width=160 * mm,
                height=70 * mm
            )
        )

    # DATA QUALITY CONCLUSION

    elements.append(
        Paragraph(
            "Data Quality Conclusion",
            heading_style
        )
    )

    if completeness >= 95 and duplicates == 0 and whitespace_issues == 0:

        conclusion = (
            "The dataset shows a good level of data quality. "
            "No major completeness or consistency issues were detected."
        )

    elif completeness >= 80:

        conclusion = (
            "The dataset has an acceptable level of completeness, "
            "but some data quality issues should be reviewed."
        )

    else:

        conclusion = (
            "The dataset requires attention. Significant missing values "
            "or consistency issues may affect the analysis."
        )

    elements.append(
        Paragraph(
            conclusion,
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Consistency issues count duplicate rows and text values "
            "with leading or trailing whitespace. A row and a cell "
            "can both contribute to this indicator.",
            styles["Normal"]
        )
    )

    # MISSING VALUES BY COLUMN
    elements.append(
        Paragraph("3. Missing Values by Column", heading_style)
    )

    missing_by_column = dataframe.isnull().sum()
    missing_by_column = missing_by_column[
        missing_by_column > 0
    ].sort_values(ascending=False)

    if not missing_by_column.empty:

        missing_data = [
            ["Column", "Missing Values", "Completeness"]
        ]

        for column, count in missing_by_column.head(20).items():

            column_completeness = (
                (total_rows - count) / total_rows * 100
                if total_rows > 0 else 0
            )

            missing_data.append([
                str(column)[:35],
                int(count),
                f"{column_completeness:.1f}%"
            ])

        missing_table = Table(
            missing_data,
            colWidths=[75 * mm, 45 * mm, 45 * mm]
        )

        missing_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("PADDING", (0, 0), (-1, -1), 6)
            ])
        )

        elements.append(missing_table)

        if len(missing_by_column) > 20:
            elements.append(
                Paragraph(
                    "Only the first 20 columns with missing values are shown.",
                    styles["Italic"]
                )
            )

    else:

        elements.append(
            Paragraph(
                "No missing values detected in this dataset.",
                styles["Normal"]
            )
        )
        # DATA TYPES DISTRIBUTION

    elements.append(
        Paragraph("4. Data Types Distribution", heading_style)
    )

    dtype_counts = (
        dataframe.dtypes.astype(str)
        .value_counts()
    )

    dtype_data = [
        ["Data Type", "Number of Columns", "Percentage"]
    ]

    for dtype, count in dtype_counts.items():

        percentage = (
            count / total_columns * 100
            if total_columns > 0 else 0
        )

        dtype_data.append([
            str(dtype),
            int(count),
            f"{percentage:.1f}%"
        ])

    dtype_table = Table(
        dtype_data,
        colWidths=[65 * mm, 65 * mm, 35 * mm]
    )

    dtype_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )

    elements.append(dtype_table)

    # STATISTICAL SUMMARY
    elements.append(
        Paragraph("5. Statistical Summary", heading_style)
    )

    summary = dataframe.describe(
        include="all"
    ).T.fillna("-")

    summary_data = [
        ["Column", "Type", "Count", "Mean", "Std", "Min", "Max"]
    ]

    for column, row in summary.head(15).iterrows():

        summary_data.append([
            str(column)[:18],
            str(dataframe[column].dtype),
            str(row.get("count", "-"))[:12],
            str(row.get("mean", "-"))[:12],
            str(row.get("std", "-"))[:12],
            str(row.get("min", "-"))[:12],
            str(row.get("max", "-"))[:12]
        ])

    summary_table = Table(
        summary_data,
        repeatRows=1
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ])
    )

    elements.append(summary_table)

    if len(summary) > 15:
        elements.append(
            Paragraph(
                "Statistical summary limited to the first 15 columns.",
                styles["Italic"]
            )
        )

    # FOOTER
    def add_footer(canvas, doc):

        canvas.saveState()

        canvas.setStrokeColor(
            colors.HexColor("#E2E8F0")
        )

        canvas.line(
            18 * mm,
            15 * mm,
            192 * mm,
            15 * mm
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        canvas.drawString(
            18 * mm,
            10 * mm,
            "DataVision | Data Analytics Platform"
        )

        canvas.drawRightString(
            192 * mm,
            10 * mm,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    document.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    buffer.seek(0)

    return buffer


# ============================================
# 5. SIDEBAR
# ============================================

st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="brand-icon">📊</div>
    <div>
        <h2>DataVision</h2>
        <p>Data Analytics Platform</p>
    </div>
</div>

<div class="sidebar-section">WORKSPACE</div>
""", unsafe_allow_html=True)


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Explorer",
        "Statistics",
        "Visualization",
        "Data Cleaning",
        "Data Quality",
        "PDF Report",
        "About"
    ],
    label_visibility="collapsed"
)


st.sidebar.divider()

st.sidebar.subheader("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is not None:

    if st.session_state.source_name != uploaded_file.name:

        try:

            new_df = load_dataset(uploaded_file)

            if new_df is not None:

                st.session_state.df = new_df
                st.session_state.cleaned_df = new_df.copy()
                st.session_state.source_name = uploaded_file.name

                st.sidebar.success("Dataset loaded successfully!")

        except Exception as error:

            st.sidebar.error(f"Error loading dataset: {error}")


if st.session_state.df is not None:

    st.sidebar.caption(
        f"Current file: {st.session_state.source_name}"
    )

    st.sidebar.caption(
        f"{st.session_state.df.shape[0]:,} rows × "
        f"{st.session_state.df.shape[1]} columns"
    )


# ============================================
# 6. MAIN HEADER
# ============================================

st.title("📊 DataVision")

st.caption(
    "Explore, analyze and visualize your data."
)

st.divider()

# ============================================
# 7. CHECK DATASET
# ============================================

if st.session_state.df is None and page != "About":

    st.info(
        "👈 Upload a CSV or Excel dataset from the sidebar to get started."
    )

    st.markdown("### Welcome to DataVision")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📈 Analytics")
        st.write("Understand your dataset with statistical analysis.")

    with col2:
        st.markdown("### 📊 Visualization")
        st.write("Create interactive charts and explore your data.")

    with col3:
        st.markdown("### 🧹 Data Cleaning")
        st.write("Detect missing values and clean your dataset.")

    st.stop()


df = st.session_state.df
cleaned_df = st.session_state.cleaned_df


# ============================================
# 8. DASHBOARD
# ============================================


if page == "Dashboard":

    # HEADER
    st.header("Dashboard Overview")

    st.caption(
        f"Welcome to your workspace | Dataset: {st.session_state.source_name}"
    )

    # KPI CALCULATIONS
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    total_cells = df.size

    quality_score = (
        ((total_cells - missing_values) / total_cells) * 100
        if total_cells > 0 else 0
    )

    # KPI CARDS
    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📊 Total Rows",
            f"{total_rows:,}"
        )

    with col2:
        st.metric(
            "📁 Total Columns",
            total_columns
        )

    with col3:
        st.metric(
            "⚠️ Missing Values",
            f"{missing_values:,}"
        )

    with col4:
        st.metric(
            "🔄 Duplicates",
            f"{duplicates:,}"
        )

    st.divider()

    # DATA QUALITY SECTION
    st.subheader("Data Quality")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("Dataset Completeness")
        st.progress(quality_score / 100)

    with col2:
        st.metric(
            "Completeness Score",
            f"{quality_score:.1f}%"
        )

    st.divider()

    # CHARTS SECTION
    st.subheader("Data Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Column Data Types**")

        type_counts = (
            df.dtypes.astype(str)
            .value_counts()
            .reset_index()
        )

        type_counts.columns = ["Data Type", "Count"]

        fig = px.pie(
            type_counts,
            names="Data Type",
            values="Count",
            hole=0.55,
            color_discrete_sequence=[
                "#2563EB",
                "#60A5FA",
                "#93C5FD",
                "#1D4ED8"
            ]
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with col2:

        st.markdown("**Missing Values by Column**")

        missing_data = (
            df.isnull()
            .sum()
            .reset_index()
        )

        missing_data.columns = [
            "Column",
            "Missing Values"
        ]

        missing_data = missing_data[
            missing_data["Missing Values"] > 0
        ]

        if not missing_data.empty:

            fig = px.bar(
                missing_data,
                x="Column",
                y="Missing Values",
                color_discrete_sequence=["#2563EB"]
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        else:

            st.success("Excellent! No missing values detected.")

    st.divider()

    # DATASET PREVIEW
    st.subheader("Dataset Preview")

    st.caption("Explore the first 10 rows of your dataset.")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()


# ============================================
# 9. DATA EXPLORER
# ============================================


elif page == "Data Explorer":

    st.header("🔍 Data Explorer")
    st.caption("Explore, search and filter your dataset.")

    # ==================================
    # DATASET OVERVIEW
    # ==================================

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")

    with col2:
        st.metric("Total Columns", df.shape[1])

    with col3:
        st.metric(
            "Memory Usage",
            f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        )

    st.divider()

    # ==================================
    # SEARCH
    # ==================================

    st.subheader("Search Dataset")

    search_query = st.text_input(
        "Search across all columns",
        placeholder="Enter a keyword..."
    )

    filtered_df = df.copy()

    if search_query.strip():

        mask = filtered_df.astype(str).apply(
            lambda column: column.str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
        ).any(axis=1)

        filtered_df = filtered_df[mask]

    st.caption(
        f"Found {len(filtered_df):,} matching rows"
    )

    st.divider()

    # ==================================
    # FILTERS AND COLUMN SELECTION
    # ==================================

    st.subheader("Filters & Display Options")

    col1, col2 = st.columns(2)

    with col1:

        selected_columns = st.multiselect(
            "Select columns to display",
            options=df.columns.tolist(),
            default=df.columns.tolist()
        )

    with col2:

        filter_column = st.selectbox(
            "Filter by column",
            options=["No filter"] + df.columns.tolist()
        )

    if filter_column != "No filter":

        unique_values = filtered_df[filter_column].dropna().unique()

        if len(unique_values) > 0:

            selected_value = st.selectbox(
                f"Select value from {filter_column}",
                options=unique_values.tolist()
            )

            filtered_df = filtered_df[
                filtered_df[filter_column] == selected_value
            ]

        else:

            st.info("No values available for this filter.")

    st.divider()

    # ==================================
    # TABLE PREVIEW
    # ==================================

    st.subheader("Dataset Preview")

    if not selected_columns:

        st.warning("Please select at least one column.")

    else:

        col1, col2 = st.columns([1, 2])

        with col1:

            rows_to_display = st.selectbox(
                "Rows per page",
                [10, 25, 50, 100]
            )

        with col2:

            st.write(
                f"**{len(filtered_df):,}** matching rows"
            )

        display_df = filtered_df[selected_columns]

        st.dataframe(
            display_df.head(rows_to_display),
            use_container_width=True,
            height=400
        )

        # ==================================
        # DOWNLOAD
        # ==================================

        st.download_button(
            label="⬇️ Download Filtered Dataset",
            data=display_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )

    st.divider()

    # ==================================
    # COLUMN INFORMATION
    # ==================================

    st.subheader("Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Values": df.notnull().sum().values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )


# ============================================
# 10. STATISTICS
# ============================================

elif page == "Statistics":

    st.header("📐 Statistical Analysis")

    st.caption("Discover statistical insights from your numerical data.")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:

        st.warning("No numerical columns found in this dataset.")

    else:

        st.subheader("Descriptive Statistics")

        st.dataframe(
            numeric_df.describe().T,
            use_container_width=True
        )

        st.divider()

        selected_column = st.selectbox(
            "Select a numerical column",
            numeric_df.columns
        )

        series = numeric_df[selected_column].dropna()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Mean",
            f"{series.mean():.2f}" if not series.empty else "N/A"
        )

        col2.metric(
            "Median",
            f"{series.median():.2f}" if not series.empty else "N/A"
        )

        col3.metric(
            "Variance",
            f"{series.var():.2f}" if len(series) > 1 else "N/A"
        )

        col4.metric(
            "Standard Deviation",
            f"{series.std():.2f}" if len(series) > 1 else "N/A"
        )

        st.divider()

        st.subheader("Correlation Between Variables")

        if numeric_df.shape[1] >= 2:

            correlation = numeric_df.corr()

            fig = px.imshow(
                correlation,
                text_auto=True,
                color_continuous_scale="Blues",
                title="Correlation Matrix"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )

        else:

            st.info("At least two numerical columns are required for correlation analysis.")


# ============================================
# 11. VISUALIZATION
# ============================================

elif page == "Visualization":

    st.header("📊 Data Visualization")

    st.caption("Create interactive visualizations from your dataset.")

    chart_type = st.selectbox(
        "Choose Visualization Type",
        [
            "Histogram",
            "Bar Chart",
            "Pie Chart",
            "Line Chart",
            "Scatter Plot",
            "Box Plot"
        ]
    )

    all_columns = df.columns.tolist()

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    fig = None

    # HISTOGRAM
    if chart_type == "Histogram":

        if numeric_columns:

            column = st.selectbox(
                "Select numerical column",
                numeric_columns
            )

            fig = px.histogram(
                df,
                x=column,
                title=f"Distribution of {column}",
                color_discrete_sequence=["#2563EB"]
            )

        else:

            st.warning("No numerical columns available.")

    # BAR CHART
    elif chart_type == "Bar Chart":

        column = st.selectbox(
            "Select column",
            all_columns
        )

        bar_data = (
            df[column]
            .astype(str)
            .value_counts()
            .head(20)
            .reset_index()
        )

        bar_data.columns = [column, "Count"]

        fig = px.bar(
            bar_data,
            x=column,
            y="Count",
            title=f"Count by {column}",
            color_discrete_sequence=["#2563EB"]
        )

    # PIE CHART
    elif chart_type == "Pie Chart":

        column = st.selectbox(
            "Select column",
            all_columns
        )

        pie_data = (
            df[column]
            .astype(str)
            .value_counts()
            .head(10)
            .reset_index()
        )

        pie_data.columns = [column, "Count"]

        fig = px.pie(
            pie_data,
            names=column,
            values="Count",
            title=f"Distribution of {column}",
            color_discrete_sequence=[
                "#2563EB",
                "#60A5FA",
                "#93C5FD",
                "#1D4ED8",
                "#BFDBFE"
            ]
        )

    # LINE CHART
    elif chart_type == "Line Chart":

        if numeric_columns:

            column = st.selectbox(
                "Select numerical column",
                numeric_columns
            )

            fig = px.line(
                df,
                y=column,
                title=f"Line Chart - {column}",
                color_discrete_sequence=["#2563EB"]
            )

        else:

            st.warning("No numerical columns available.")

    # SCATTER PLOT
    elif chart_type == "Scatter Plot":

        if len(numeric_columns) >= 2:

            col1, col2 = st.columns(2)

            with col1:
                x_column = st.selectbox(
                    "X Axis",
                    numeric_columns
                )

            available_y = [
                col for col in numeric_columns
                if col != x_column
            ]

            with col2:
                y_column = st.selectbox(
                    "Y Axis",
                    available_y
                )

            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{x_column} vs {y_column}",
                color_discrete_sequence=["#2563EB"]
            )

        else:

            st.warning("At least two numerical columns are required.")

    # BOX PLOT
    elif chart_type == "Box Plot":

        if numeric_columns:

            column = st.selectbox(
                "Select numerical column",
                numeric_columns
            )

            fig = px.box(
                df,
                y=column,
                title=f"Box Plot - {column}",
                color_discrete_sequence=["#2563EB"]
            )

        else:

            st.warning("No numerical columns available.")

    if fig is not None:

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        st.success("Visualization generated successfully!")


# ============================================
# 12. DATA CLEANING
# ============================================


elif page == "Data Cleaning":

    st.header("🧹 Data Cleaning")

    st.caption(
        "Prepare your dataset by handling missing values and duplicates."
    )

    original_df = st.session_state.df
    cleaned_df = st.session_state.cleaned_df

    # ==================================
    # CLEANING METRICS
    # ==================================

    st.subheader("Cleaning Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Original Rows", f"{len(original_df):,}")

    with col2:
        st.metric("Current Rows", f"{len(cleaned_df):,}")

    with col3:
        st.metric(
            "Missing Values",
            f"{cleaned_df.isnull().sum().sum():,}"
        )

    with col4:
        st.metric(
            "Duplicates",
            f"{cleaned_df.duplicated().sum():,}"
        )

    st.divider()

    # ==================================
    # SELECT CLEANING OPERATION
    # ==================================

    st.subheader("1. Choose Cleaning Operation")

    operation = st.selectbox(
        "Select an operation",
        [
            "Select an operation",
            "Remove Missing Rows",
            "Fill Numeric Values with Median",
            "Fill Missing Values with Mode",
            "Remove Duplicate Rows"
        ]
    )

    # ==================================
    # PREVIEW OPERATION
    # ==================================

    preview_df = cleaned_df.copy()

    if operation == "Remove Missing Rows":

        preview_df = preview_df.dropna()

    elif operation == "Fill Numeric Values with Median":

        numeric_cols = preview_df.select_dtypes(
            include=np.number
        ).columns

        preview_df[numeric_cols] = preview_df[numeric_cols].fillna(
            preview_df[numeric_cols].median()
        )

    elif operation == "Fill Missing Values with Mode":

        for col in preview_df.columns:

            if preview_df[col].isnull().any():

                modes = preview_df[col].mode()

                if not modes.empty:

                    preview_df[col] = preview_df[col].fillna(
                        modes.iloc[0]
                    )

    elif operation == "Remove Duplicate Rows":

        preview_df = preview_df.drop_duplicates()

    # ==================================
    # PREVIEW COMPARISON
    # ==================================

    if operation != "Select an operation":

        st.subheader("2. Preview Changes")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Before Cleaning**")

            st.metric(
                "Rows",
                f"{len(cleaned_df):,}"
            )

            st.metric(
                "Missing Values",
                int(cleaned_df.isnull().sum().sum())
            )

            st.metric(
                "Duplicates",
                int(cleaned_df.duplicated().sum())
            )

        with col2:

            st.markdown("**After Cleaning**")

            st.metric(
                "Rows",
                f"{len(preview_df):,}",
                delta=f"{len(preview_df) - len(cleaned_df):,} rows"
            )

            st.metric(
                "Missing Values",
                int(preview_df.isnull().sum().sum()),
                delta=(
                    int(preview_df.isnull().sum().sum())
                    - int(cleaned_df.isnull().sum().sum())
                )
            )

            st.metric(
                "Duplicates",
                int(preview_df.duplicated().sum()),
                delta=(
                    int(preview_df.duplicated().sum())
                    - int(cleaned_df.duplicated().sum())
                )
            )

        with st.expander("View preview dataset"):

            st.dataframe(
                preview_df.head(10),
                use_container_width=True
            )

        # ==================================
        # APPLY OPERATION
        # ==================================

        st.divider()

        if st.button(
            "Apply Cleaning Operation",
            type="primary"
        ):

            st.session_state.cleaned_df = preview_df.copy()

            st.success(
                f"{operation} applied successfully!"
            )

            st.rerun()

    else:

        st.info("Select a cleaning operation to preview its impact.")

    # ==================================
    # FINAL CLEANED DATASET
    # ==================================

    st.divider()

    st.subheader("3. Cleaned Dataset")

    cleaned_df = st.session_state.cleaned_df

    st.dataframe(
        cleaned_df.head(10),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇️ Download Cleaned CSV",
            data=cleaned_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    with col2:

        if st.button("↩️ Reset Original Dataset"):

            st.session_state.cleaned_df = original_df.copy()

            st.success("Dataset restored successfully!")

            st.rerun()



# ============================================
# 13. DATA QUALITY
# ============================================

elif page == "Data Quality":

    st.header("🔍 Data Quality Dashboard")
    st.caption(
        "Analyze completeness, validity and consistency "
        "to understand the quality of your dataset."
    )

    # Use the current cleaned dataset
    quality_df = st.session_state.cleaned_df.copy()

    if quality_df.empty or quality_df.shape[1] == 0:
        st.warning("Your dataset is empty. Please upload valid data.")
    else:

        total_cells = quality_df.size
        missing_cells = int(quality_df.isnull().sum().sum())
        complete_cells = total_cells - missing_cells

        # 1. COMPLETENESS
        completeness = (
            complete_cells / total_cells * 100
            if total_cells > 0 else 0
        )

        # 2. VALIDITY CHECKS
        validation_results = []

        for col in quality_df.columns:

            col_name = str(col).lower()
            non_null = quality_df[col].dropna()

            # Email validation
            if "email" in col_name:
                invalid_count = int(
    (~non_null.astype(str).str.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+"
    )).sum()
)

                validation_results.append({
                    "Column": col,
                    "Validation Rule": "Valid email format",
                    "Invalid Values": invalid_count,
                    "Checked Values": len(non_null)
                })

            # Negative values in common non-negative fields
            elif any(
                word in col_name
                for word in [
                    "age", "salary", "price",
                    "amount", "revenue", "quantity", "income"
                ]
            ) and pd.api.types.is_numeric_dtype(quality_df[col]):

                invalid_count = int((non_null < 0).sum())

                validation_results.append({
                    "Column": col,
                    "Validation Rule": "No negative values",
                    "Invalid Values": invalid_count,
                    "Checked Values": len(non_null)
                })

        if validation_results:
            validation_df = pd.DataFrame(validation_results)

            total_checked = int(validation_df["Checked Values"].sum())
            total_invalid = int(validation_df["Invalid Values"].sum())

            validity = (
                (total_checked - total_invalid) / total_checked * 100
                if total_checked > 0 else None
            )
        else:
            validation_df = pd.DataFrame()
            validity = None

        # 3. CONSISTENCY CHECKS
        object_cols = quality_df.select_dtypes(
            include=["object", "string"]
        ).columns

        whitespace_issues = 0

        for col in object_cols:
            values = quality_df[col].dropna().astype(str)

            whitespace_issues += int(
                values.str.contains(r"^\s|\s$", regex=True).sum()
            )

        duplicate_count = int(quality_df.duplicated().sum())

        consistency_issues = whitespace_issues + duplicate_count

        consistency_denominator = total_cells + len(quality_df)

        consistency = (
            max(
                0,
                (1 - consistency_issues / consistency_denominator) * 100
            )
            if consistency_denominator > 0 else 0
        )

        # QUALITY OVERVIEW
        st.subheader("Quality Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Completeness",
                f"{completeness:.1f}%"
            )

        with col2:
            st.metric(
                "Validity",
                f"{validity:.1f}%" if validity is not None else "N/A"
            )

        with col3:
            st.metric(
                "Consistency Indicator",
                f"{consistency:.1f}%"
            )
            st.caption(
                "Internal score based on duplicates and whitespace issues."
            )
        with col4:
            st.metric(
                "Missing Values",
                f"{missing_cells:,}"
            )

        st.divider()

        # COMPLETENESS DETAILS
        st.subheader("1. Completeness Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Dataset Completeness**")
            st.progress(completeness / 100)
            st.write(f"{complete_cells:,} complete cells out of {total_cells:,}")

        with col2:
            st.markdown("**Missing Values Summary**")
            st.metric(
                "Missing Values",
                f"{missing_cells:,}"
            )
            st.metric(
                "Complete Values",
                f"{complete_cells:,}"
            )

        # COMPLETENESS BY COLUMN
        missing_by_column = quality_df.isnull().sum()

        column_quality = pd.DataFrame({
            "Column": missing_by_column.index.astype(str),
            "Missing Values": missing_by_column.values,
            "Completeness (%)": [
                (1 - missing / len(quality_df)) * 100
                for missing in missing_by_column.values
            ]
        })
                # DATA QUALITY ALERTS
        st.divider()
        st.subheader("🚨 Data Quality Alerts")

        alerts = []

        # Missing values alerts
        for _, row in column_quality.iterrows():

            if row["Missing Values"] > 0:
                alerts.append({
                    "Level": "Warning",
                    "Issue": "Missing Values",
                    "Column": row["Column"],
                    "Details": f'{int(row["Missing Values"])} missing value(s)'
                })

        # Invalid values alerts
        if not validation_df.empty:

            for _, row in validation_df.iterrows():

                if row["Invalid Values"] > 0:
                    alerts.append({
                        "Level": "Critical",
                        "Issue": "Invalid Values",
                        "Column": row["Column"],
                        "Details": (
                            f'{int(row["Invalid Values"])} invalid value(s) '
                            f'({row["Validation Rule"]})'
                        )
                    })

        # Duplicate rows alert
        if duplicate_count > 0:
            alerts.append({
                "Level": "Warning",
                "Issue": "Duplicate Rows",
                "Column": "Dataset",
                "Details": f"{duplicate_count} duplicate row(s) detected"
            })

        # Whitespace alert
        if whitespace_issues > 0:
            alerts.append({
                "Level": "Warning",
                "Issue": "Whitespace",
                "Column": "Text Columns",
                "Details": f"{whitespace_issues} value(s) with extra spaces"
            })

        # Display alerts
        if alerts:

            alerts_df = pd.DataFrame(alerts)

            for _, alert in alerts_df.iterrows():

                if alert["Level"] == "Critical":
                    st.error(
                        f'🔴 **{alert["Issue"]} — {alert["Column"]}**\n\n'
                        f'{alert["Details"]}'
                    )
                else:
                    st.warning(
                        f'🟠 **{alert["Issue"]} — {alert["Column"]}**\n\n'
                        f'{alert["Details"]}'
                    )

            st.caption(
                f"{len(alerts)} potential data quality issue(s) detected."
            )

            st.download_button(
                "⬇️ Download Quality Alerts",
                data=alerts_df.to_csv(index=False).encode("utf-8"),
                file_name="data_quality_alerts.csv",
                mime="text/csv"
            )

        else:
            st.success(
                "Excellent! No issues were detected by the current checks."
            )

        st.markdown("**Completeness by Column**")

        fig = px.bar(
            column_quality.sort_values("Completeness (%)"),
            x="Completeness (%)",
            y="Column",
            orientation="h",
            color="Completeness (%)",
            color_continuous_scale="Blues",
            range_x=[0, 100],
            title="Completeness Percentage per Column"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        st.divider()

        # VALIDITY DETAILS
        st.subheader("2. Validity Analysis")

        if not validation_df.empty:

            st.write(
                f"Checked {total_checked:,} values "
                f"and found {total_invalid:,} invalid values."
            )

            st.dataframe(
                validation_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "No automatic validation rules were applicable. "
                "Try columns containing 'email', 'age', 'price', "
                "'salary' or similar names."
            )

        st.divider()

        # CONSISTENCY DETAILS
        st.subheader("3. Consistency Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Duplicate Rows",
                f"{duplicate_count:,}"
            )

        with col2:
            st.metric(
                "Whitespace Issues",
                f"{whitespace_issues:,}"
            )

        with col3:
            st.metric(
                "Consistency Issues",
                f"{consistency_issues:,}"
            )

        st.caption(
            "Consistency checks count duplicate rows and text values "
            "with leading or trailing spaces. A row and a cell can "
            "both contribute to this indicator."
        )

        st.divider()

        # COLUMN QUALITY REPORT
        st.subheader("4. Column Quality Report")

        st.dataframe(
            column_quality.sort_values(
                "Completeness (%)",
                ascending=True
            ),
            use_container_width=True,
            hide_index=True
        )

        # DOWNLOAD REPORT
        st.divider()
        st.subheader("5. Export Quality Report")

        report_csv = column_quality.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Column Quality Report",
            data=report_csv,
            file_name="data_quality_report.csv",
            mime="text/csv"
        )

# ============================================
# 14. PDF REPORT
# ============================================

elif page == "PDF Report":

    st.header("📄 PDF Report")

    st.caption("Generate a PDF summary of your dataset.")

    st.subheader("Report Preview")

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    total_cells = df.size

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    completeness = (
        (total_cells - missing_values) / total_cells * 100
        if total_cells > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Rows",
        f"{total_rows:,}"
    )

    col2.metric(
        "Total Columns",
        total_columns
    )

    col3.metric(
        "Completeness",
        f"{completeness:.1f}%"
    )

    col4.metric(
        "Duplicate Rows",
        duplicate_rows
    )
    st.divider()

    st.subheader("Statistical Summary")

    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True
    )

    st.divider()

    if st.button("Generate PDF Report"):

        try:

            pdf_file = create_pdf_report(df)

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_file,
                file_name="DataVision_Report.pdf",
                mime="application/pdf"
            )

            st.success("PDF report generated successfully!")

        except Exception as error:

            st.error(f"Could not generate PDF: {error}")

elif page == "About":

    st.title("🚀 About DataVision")

    st.caption(
        "A modern platform for data analysis, visualization and quality assessment."
    )

    st.divider()

    # PROJECT OVERVIEW
    st.subheader("📊 Project Overview")

    st.markdown("""
    **DataVision** is an interactive data analytics platform
    designed to help users explore, analyze, clean and
    visualize their datasets.

    The platform transforms raw data into meaningful insights
    through an intuitive and user-friendly interface.
    """)

    st.divider()

    # MAIN FEATURES
    st.subheader("✨ Main Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📈 Data Analysis")

        st.write("""
        - Interactive Dashboard
        - Descriptive Statistics
        - Correlation Analysis
        - Data Exploration
        """)

        st.markdown("### 🧹 Data Cleaning")

        st.write("""
        - Missing Values Handling
        - Duplicate Removal
        - Data Cleaning Preview
        - Cleaned Dataset Export
        """)

    with col2:

        st.markdown("### 📊 Data Visualization")

        st.write("""
        - Histogram
        - Bar Chart
        - Pie Chart
        - Line Chart
        - Scatter Plot
        - Box Plot
        """)

        st.markdown("### 🔍 Data Quality")

        st.write("""
        - Completeness Analysis
        - Validity Checks
        - Consistency Analysis
        - Quality Alerts
        - Column Quality Report
        """)

    st.divider()

    # TECHNOLOGIES
    st.subheader("🛠️ Technologies Used")

    technologies = [
        "Python",
        "Streamlit",
        "Pandas",
        "NumPy",
        "Plotly",
        "ReportLab"
    ]

    cols = st.columns(3)

    for i, tech in enumerate(technologies):

        with cols[i % 3]:
            st.info(f"**{tech}**")

    st.divider()

    # PROJECT LINKS
    st.subheader("🔗 Project Resources")

    col1, col2 = st.columns(2)

    with col1:

        st.link_button(
            "🌐 GitHub Repository",
            "https://github.com/17DOS3/DataVision",
            use_container_width=True
        )

    with col2:

        st.link_button(
            "🚀 Live Demo",
            "https://datavision-ufmezbl8zywa62ym4sf99f.streamlit.app/",
            use_container_width=True
        )

    st.divider()

    # FOOTER
    st.markdown(
        """
        <div style="text-align:center; padding:20px; color:#64748B;">
            <h4>DataVision</h4>
            <p>Turning Data into Insights.</p>
            <small>Data Analytics & Visualization Project</small>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================
# 15. FOOTER
# ============================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94A3B8; font-size:12px;">
        DataVision | Data Analytics Platform
        <br>
        Built with Python, Pandas, Plotly and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
