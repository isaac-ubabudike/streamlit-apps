#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

#App Setup
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.write("Transform your files between csv and excel format with built-in cleaning and visualization!")

#File Upload
uploaded_file = st.file_uploader("Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = df.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file.ext}")
            continue

        #display info about file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")

        #Show five rows of our dataframe
        st.write(f"**Preview the Head of the DataFrame**")
        st.dataframe(df.head())

        #Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates for {file.name}"):
                    df = df.drop_duplicates()
                    st.write(f"Removed duplicates from {file.name}")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"Filled missing values for {file.name}")

        # Choose Specific Columns to Convert
        st.subheader("Choose Specific Columns to Convert")
        columns = st.multiselect(f"Select columns to convert for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Sample visualizations
        st.subheader("📊 Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, 0])
            st.line_chart(df.select_dtypes(include=["number"]).iloc[:, 0])

        # Convert the File --> CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ("CSV", "Excel"), key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = f"{file.name}.csv"
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = f"{file.name}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
 
            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}", 
                data=buffer,
                filename=file_name,
                mime=mime_type
            )

            st.success(f"🎉 All Files Have Been Successfully Processed!")