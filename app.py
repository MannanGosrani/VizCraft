import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import sweetviz as sv
import tempfile
import streamlit.components.v1 as components

st.set_page_config(page_title="CSV Data Analyzer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #ffffff;'>📊 VizCraft: CSV Data Analysis </h1>", unsafe_allow_html=True)


# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV uploaded successfully!")

    # Extract column types
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Tabs for clean navigation
    tab1, tab2, tab3 = st.tabs(["📄 Overview", "📊 Visualizations", "🧠 Report"])

    # ==================== Tab 1: Overview ====================
    with tab1:
        st.markdown("### 🧾 Data Overview")

        with st.expander("📋 Show Raw Data"):
            st.dataframe(df)

        with st.expander("🔍 Dataset Info"):
            st.markdown(f"- **Shape:** {df.shape}")
            st.markdown("#### Data Types")
            st.write(df.dtypes)
            st.markdown("#### Missing Values")
            st.write(df.isnull().sum())

        with st.expander("📈 Summary Statistics"):
            st.write(df.describe())

    # ==================== Tab 2: Visualizations ====================
    with tab2:
        st.markdown("### 📊 Explore Your Data")

        # Numeric Visualization
        if numeric_cols:
            st.markdown("#### 📈 Visualize Numeric Column")
            selected_num = st.selectbox("Choose a numeric column", numeric_cols, key="num_col")
            chart_type_num = st.radio("Select chart type", ["Histogram", "Line Chart"], horizontal=True, key="num_type")

            if chart_type_num == "Histogram":
                fig = px.histogram(
                    df,
                    x=selected_num,
                    nbins=30,
                    title=f"Histogram of {selected_num}",
                    text_auto=True  
                )
                fig.update_traces(
                    marker_line_color="black",  
                    marker_line_width=1.5       
                )
                fig.update_layout(
                    bargap=0.1,  
                    xaxis_title=selected_num,
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type_num == "Line Chart":
                fig = px.line(df, y=selected_num, title=f"Line Chart of {selected_num}")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available for visualization.")

        # Categorical Visualization
        if cat_cols:
            st.markdown("#### 📊 Visualize Categorical Column")
            selected_cat = st.selectbox("Choose a categorical column", cat_cols, key="cat_col")
            chart_type_cat = st.radio("Select chart type", ["Count Plot", "Pie Chart"], horizontal=True, key="cat_type")

            if chart_type_cat == "Count Plot":
                fig2 = px.histogram(df, x=selected_cat, color=selected_cat, title=f"Count Plot of {selected_cat}")
                st.plotly_chart(fig2, use_container_width=True)
            elif chart_type_cat == "Pie Chart":
                pie_df = df[selected_cat].value_counts().reset_index()
                pie_df.columns = [selected_cat, 'Count']
                fig2 = px.pie(pie_df, names=selected_cat, values='Count', title=f"Pie Chart of {selected_cat}")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No categorical columns available for visualization.")


    # ==================== Tab 3: Report ====================
    with tab3:
        st.markdown("### 🧠 Generate Data Profiling Report")
        if st.button("Generate Sweetviz Report"):
            with st.spinner("Generating Sweetviz report..."):
                report = sv.analyze(df)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                    report.show_html(tmpfile.name, open_browser=False)
                    st.success("✅ Report generated below ⬇️")
                    with open(tmpfile.name, 'r', encoding='utf-8') as f:
                        html = f.read()
                        components.html(html, height=1000, scrolling=True)

    # Footer
    st.markdown("---")
    st.markdown("Made by Mannan Gosrani • © 2025")

else:
    st.warning("📂 Please upload a CSV file to begin.")
