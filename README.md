# VizCraft – CSV Data Analysis Web App

VizCraft is an interactive web application that allows users to upload CSV files and instantly visualize, explore, and profile their data using a clean dashboard. Built with Streamlit, this app is ideal for data analysts, students, and professionals who want quick insights from their datasets without writing code.

## Overview

VizCraft simplifies the process of data analysis by providing:

- A responsive UI with tab-based navigation
- Instant visualizations for both numeric and categorical data
- Automated data profiling using Sweetviz
- Interactive plots using Plotly, Seaborn, and Matplotlib

Whether you're exploring datasets for a project, preparing reports, or experimenting with CSV files, VizCraft helps turn raw data into meaningful insights.

## Features

### File Upload & Parsing
- Upload CSV files of any size upto 200MB
- Automatically detects column types (numeric and categorical)

### Tab 1: Overview
- View raw data and dataset shape
- See data types and missing values
- Get summary statistics

### Tab 2: Visualizations
- Numeric columns: Histogram, Line chart
- Categorical columns: Count plot, Pie chart
- Correlation heatmap for numeric features

### Tab 3: Data Profiling Report
- Generates a full exploratory data analysis report using Sweetviz
- Report is viewable directly within the app

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Matplotlib
- Seaborn
- Sweetviz

## Customizing Theme with `.streamlit/config.toml`

To customize the appearance of VizCraft, you can create a `.streamlit` folder in your project directory and add a `config.toml` file with your desired theme settings.

### Steps:

1. Create the folder named " .streamlit ".

2. Inside the .streamlit/ folder, add the files(.toml) already provided in the repository.

3. To change the theme, simply modify the " .config/toml " file by the ones provided in the repository or any value of your choice . Save and re-run the application to make the changes
