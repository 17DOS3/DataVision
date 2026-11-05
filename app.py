
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="DataVision",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #171b26;
}
.metric-card {
    background: #1b2230;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #30394a;
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 DataVision")
st.sidebar.caption("Data Analytics Platform")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Explorer",
        "Statistics",
        "Visualization",
        "Data Cleaning",
        "Data Quality",
        "PDF Report"
    ]
)

st.title("📊 DataVision")
st.caption("Explore, analyze and visualize your data.")

# Upload CSV or Excel
uploaded_file = st.sidebar.file_uploader(
    "Upload Your Dataset",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "csv":
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="latin-1")

        else:
            df = pd.read_excel(uploaded_file)

        st.sidebar.success("Dataset loaded successfully!")

        if page == "Dashboard":
            st.header("Dashboard Overview")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Rows", f"{df.shape[0]:,}")
            col2.metric("Total Columns", df.shape[1])
            col3.metric("Missing Values", int(df.isnull().sum().sum()))
            col4.metric("Duplicates", int(df.duplicated().sum()))

            st.divider()

            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)

        elif page == "Data Explorer":
            st.header("Data Explorer")
            st.dataframe(df, use_container_width=True)

            st.subheader("Column Information")
            info = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Missing Values": df.isnull().sum().values
            })
            st.dataframe(info, use_container_width=True)

        
        elif page == "Statistics":
            st.header("📈 Statistical Analysis")
            st.caption("Explore descriptive statistics and data relationships.")

            numeric_df = df.select_dtypes(include=np.number)

            if not numeric_df.empty:

                st.subheader("Descriptive Statistics")

                stats = pd.DataFrame({
                    "Mean": numeric_df.mean(),
                    "Median": numeric_df.median(),
                    "Mode": numeric_df.mode().iloc[0],
                    "Variance": numeric_df.var(),
                    "Standard Deviation": numeric_df.std(),
                    "Minimum": numeric_df.min(),
                    "Maximum": numeric_df.max()
                })

                st.dataframe(
                    stats.round(2),
                    use_container_width=True
                )

                st.divider()

                st.subheader("Correlation Matrix")

                correlation = numeric_df.corr()

                fig = px.imshow(
                    correlation,
                    text_auto=True,
                    color_continuous_scale="Purples",
                    title="Correlation Between Variables",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning("No numerical columns found.")

            st.divider()

            st.subheader("Missing Values Analysis")

            missing = df.isnull().sum()

            missing_df = pd.DataFrame({
                "Column": missing.index,
                "Missing Values": missing.values,
                "Percentage": (
                    missing.values / len(df) * 100
                ).round(2)
            })

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        
        elif page == "Data Cleaning":
            st.header("🧹 Data Cleaning")
            st.caption("Clean missing values and remove duplicate records.")

            cleaned_df = df.copy()

            st.subheader("Original Dataset")

            col1, col2, col3 = st.columns(3)
            col1.metric("Original Rows", len(df))
            col2.metric("Missing Values", int(df.isnull().sum().sum()))
            col3.metric("Duplicate Rows", int(df.duplicated().sum()))

            st.divider()

            st.subheader("1. Handle Missing Values")

            missing_strategy = st.selectbox(
                "Choose a cleaning strategy",
                [
                    "Keep missing values",
                    "Remove rows with missing values",
                    "Fill with Median / Mode"
                ]
            )

            if missing_strategy == "Remove rows with missing values":
                cleaned_df = cleaned_df.dropna()

            elif missing_strategy == "Fill with Median / Mode":
                for column in cleaned_df.columns:
                    if cleaned_df[column].isnull().any():
                        if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                            median_value = cleaned_df[column].median()
                            if pd.notna(median_value):
                                cleaned_df[column] = cleaned_df[column].fillna(median_value)
                        else:
                            mode_values = cleaned_df[column].mode()
                            if not mode_values.empty:
                                cleaned_df[column] = cleaned_df[column].fillna(mode_values.iloc[0])

            st.divider()

            st.subheader("2. Remove Duplicate Rows")

            remove_duplicates = st.checkbox(
                "Remove duplicate records",
                value=True
            )

            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()

            st.divider()

            st.subheader("3. Cleaning Results")

            col1, col2, col3 = st.columns(3)

            col1.metric("Cleaned Rows", len(cleaned_df))
            col2.metric(
                "Remaining Missing Values",
                int(cleaned_df.isnull().sum().sum())
            )
            col3.metric(
                "Remaining Duplicates",
                int(cleaned_df.duplicated().sum())
            )

            st.dataframe(cleaned_df.head(10), use_container_width=True)

            csv_data = cleaned_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Cleaned Dataset",
                data=csv_data,
                file_name="datavision_cleaned.csv",
                mime="text/csv"
            )


        
        
        elif page == "Data Quality":
            st.header("🔍 Data Quality Report")
            st.caption("Analyze completeness, duplicates, and data validation errors.")

            # Basic Quality Metrics
            total_cells = df.size
            missing_cells = int(df.isnull().sum().sum())
            complete_cells = total_cells - missing_cells

            quality_score = (
                complete_cells / total_cells * 100
                if total_cells > 0 else 0
            )

            duplicate_count = int(df.duplicated().sum())

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Completeness Score", f"{quality_score:.1f}%")
            col2.metric("Total Cells", f"{total_cells:,}")
            col3.metric("Missing Cells", f"{missing_cells:,}")
            col4.metric("Duplicate Rows", duplicate_count)

            st.divider()

            # Column Quality Analysis
            st.subheader("Column Quality Analysis")

            quality_data = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values,
                "Non-Null Values": df.notnull().sum().values,
                "Missing Values": df.isnull().sum().values,
                "Missing (%)": (
                    df.isnull().mean().values * 100
                ).round(2)
            })

            st.dataframe(quality_data, use_container_width=True)

            st.divider()

            # Missing Values Visualization
            st.subheader("Missing Values Visualization")

            missing_chart = df.isnull().sum().reset_index()
            missing_chart.columns = ["Column", "Missing Values"]

            fig = px.bar(
                missing_chart,
                x="Column",
                y="Missing Values",
                title="Missing Values per Column",
                template="plotly_dark",
                color="Missing Values",
                color_continuous_scale="Purples"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # Advanced Data Validation
            st.subheader("🚨 Advanced Data Validation")

            issues = []

            def add_issue(row_number, column, value, issue_type, description):
                issues.append({
                    "Row": row_number,
                    "Column": column,
                    "Invalid Value": str(value),
                    "Issue Type": issue_type,
                    "Description": description
                })

            for column in df.columns:

                series = df[column]
                column_name = column.lower().strip()

                # 1. Invalid Emails
                if "email" in column_name:

                    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

                    for i, value in enumerate(series):
                        if pd.notna(value):
                            if not pd.Series([str(value).strip()]).str.match(
                                email_pattern
                            ).iloc[0]:
                                add_issue(
                                    i + 2, column, value,
                                    "Invalid Email",
                                    "Email format is incorrect."
                                )

                # 2. Invalid Age
                if "age" in column_name:

                    numeric_values = pd.to_numeric(
                        series, errors="coerce"
                    )

                    for i, value in enumerate(numeric_values):
                        if pd.notna(value) and (
                            value < 0 or value > 100
                        ):
                            add_issue(
                                i + 2, column, series.iloc[i],
                                "Invalid Age",
                                "Age must be between 0 and 100."
                            )

                # 3. Negative Financial Values
                financial_keywords = [
                    "income", "salary", "price",
                    "amount", "revenue", "cost", "balance"
                ]

                if any(word in column_name for word in financial_keywords):

                    numeric_values = pd.to_numeric(
                        series, errors="coerce"
                    )

                    for i, value in enumerate(numeric_values):
                        if pd.notna(value) and value < 0:
                            add_issue(
                                i + 2, column, series.iloc[i],
                                "Negative Value",
                                "Financial value cannot be negative."
                            )

                # 4. Invalid Dates
                if "date" in column_name:

                    non_empty = series.notna() & (
                        series.astype(str).str.strip() != ""
                    )

                    parsed_dates = pd.to_datetime(
                        series,
                        errors="coerce",
                        format="mixed"
                    )

                    invalid_dates = non_empty & parsed_dates.isna()

                    for i in range(len(series)):
                        if invalid_dates.iloc[i]:
                            add_issue(
                                i + 2, column, series.iloc[i],
                                "Invalid Date",
                                "Date format is invalid."
                            )

                # 5. Unnecessary Spaces
                if series.dtype == "object":

                    for i, value in enumerate(series):
                        if pd.notna(value) and isinstance(value, str):
                            if value != value.strip():
                                add_issue(
                                    i + 2, column, value,
                                    "Extra Spaces",
                                    "Value contains unnecessary spaces."
                                )

            # Display Validation Results
            issues_df = pd.DataFrame(issues)

            issue_count = len(issues_df)

            col1, col2 = st.columns(2)

            col1.metric("Validation Errors", issue_count)

            col2.metric(
                "Columns Analyzed",
                len(df.columns)
            )

            if issue_count > 0:

                st.warning(
                    f"Found {issue_count} data quality issues."
                )

                st.dataframe(
                    issues_df,
                    use_container_width=True
                )

                st.download_button(
                    "⬇️ Download Validation Errors",
                    data=issues_df.to_csv(index=False).encode("utf-8"),
                    file_name="datavision_validation_errors.csv",
                    mime="text/csv"
                )

            else:
                st.success("No validation errors detected!")

            st.divider()

            # Export Quality Report
            st.subheader("📄 Export Quality Report")

            report = quality_data.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Quality Report",
                data=report,
                file_name="datavision_quality_report.csv",
                mime="text/csv"
            )


   


        elif page == "PDF Report":
            st.header("📄 Export PDF Report")
            st.write("Generate a summary report of your dataset.")

            if st.button("Generate PDF Report"):
                buffer = BytesIO()

                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4
                )

                styles = getSampleStyleSheet()
                elements = []

                elements.append(
                    Paragraph("DataVision - Analysis Report", styles["Title"])
                )
                elements.append(Spacer(1, 20))

                elements.append(
                    Paragraph(
                        f"Total Rows: {df.shape[0]}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Total Columns: {df.shape[1]}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Missing Values: {int(df.isnull().sum().sum())}",
                        styles["Normal"]
                    )
                )

                elements.append(
                    Paragraph(
                        f"Duplicate Rows: {int(df.duplicated().sum())}",
                        styles["Normal"]
                    )
                )

                elements.append(Spacer(1, 20))

                elements.append(
                    Paragraph("Statistical Summary", styles["Heading2"])
                )

                summary = df.describe().round(2).reset_index()

                table_data = [
                    [str(col) for col in summary.columns]
                ]

                for row in summary.values.tolist():
                    table_data.append([
                        str(value) for value in row
                    ])

                table = Table(table_data, repeatRows=1)

                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]))

                elements.append(table)

                doc.build(elements)

                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=buffer.getvalue(),
                    file_name="DataVision_Report.pdf",
                    mime="application/pdf"
                )

                st.success("PDF report generated successfully!")

        
        elif page == "Visualization":
            st.header("Data Visualization")
            st.caption("Create interactive charts from your dataset.")

            all_cols = df.columns.tolist()
            numeric_cols = df.select_dtypes(
                include=np.number
            ).columns.tolist()

            chart_type = st.selectbox(
                "Choose Chart Type",
                [
                    "Histogram",
                    "Bar Chart",
                    "Pie Chart",
                    "Line Chart",
                    "Scatter Plot",
                    "Box Plot"
                ]
            )

            if chart_type == "Histogram":
                if numeric_cols:
                    x = st.selectbox("Select numerical column", numeric_cols)
                    fig = px.histogram(
                        df, x=x, template="plotly_dark",
                        color_discrete_sequence=["#8b5cf6"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns available.")

            elif chart_type == "Bar Chart":
                x = st.selectbox("Select category", all_cols)
                y = st.selectbox(
                    "Select numerical value",
                    numeric_cols if numeric_cols else all_cols
                )
                fig = px.bar(
                    df, x=x, y=y, template="plotly_dark",
                    color_discrete_sequence=["#8b5cf6"]
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Pie Chart":
                x = st.selectbox("Select category", all_cols)
                pie_data = df[x].value_counts().reset_index()
                pie_data.columns = [x, "Count"]
                fig = px.pie(
                    pie_data, names=x, values="Count",
                    template="plotly_dark", hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Line Chart":
                if numeric_cols:
                    x = st.selectbox("Select X axis", all_cols)
                    y = st.selectbox("Select Y axis", numeric_cols)
                    fig = px.line(
                        df, x=x, y=y, markers=True,
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns available.")

            elif chart_type == "Scatter Plot":
                if len(numeric_cols) >= 2:
                    x = st.selectbox("X axis", numeric_cols)
                    y = st.selectbox(
                        "Y axis", numeric_cols,
                        index=1
                    )
                    fig = px.scatter(
                        df, x=x, y=y,
                        template="plotly_dark",
                        color_discrete_sequence=["#8b5cf6"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("You need at least two numerical columns.")

            elif chart_type == "Box Plot":
                if numeric_cols:
                    y = st.selectbox("Select numerical column", numeric_cols)
                    fig = px.box(
                        df, y=y, template="plotly_dark",
                        color_discrete_sequence=["#8b5cf6"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No numerical columns available.")

            else:
                st.warning("No numerical columns found in this dataset.")

    except Exception as error:
        st.error(f"Unable to read this dataset: {error}")

else:
    st.info("Upload a CSV or Excel dataset from the sidebar to get started.")

    st.subheader("What you can do with DataVision")

    col1, col2, col3 = st.columns(3)

    col1.markdown("### 📁 Data Explorer")
    col1.write("Explore rows, columns and missing values.")

    col2.markdown("### 📈 Statistics")
    col2.write("Analyze descriptive statistical indicators.")

    col3.markdown("### 📊 Visualization")
    col3.write("Create interactive charts and discover patterns.")
