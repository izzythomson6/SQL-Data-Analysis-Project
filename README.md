# SQL-Data-Analysis-Project
# Project Overview
This project analyses email campaign engagement data using SQL and visualises the analysis using Python. The goal of this project is to extract insights from the data which could be used in a business setting to improve campaign performance. 
# Features and analysis
**Email campaign Engagement Data:**
-Open rates, click through rates, unsubscribe rates
-Engagement trends over time (monthly)
-User level engagement analysis
-Peak days for engagement
**Techniques used:**
-Aggregate functions, CTEs, Window Functions
-Data manipulation 

**Data Visualisation:**
**Visualisations created with Python using:**
-Pandas for data manipulation
-Matplotlib & seaborn for visualisations directly from SQLite query results
**Types of visualisations included:**
-bar charts showing open rates, click-through rates, and unsubscribe rates by campaign
-Line charts displaying monthly trends in open rates across campaigns 
-Weekly engagement patterns illustrating which days of the week have higher or lower open rates

# Getting Started
1) Clone the repository
2) Ensure you have python and required packages (pandas, matplotlib, seaborn, sqlite) installed
3) Run the SQL scripts to create and populate the database
4) Execute the python visualization scripts to generate charts

# File Structure
-queries.sql - SQL queries for engagement metrics
-visualisations.py - Python scripts to generate data visualisations
-email_campaign_database.db - SQLite database file 

SQL-Data-Analysis-Project/
├── queries.sql                  # SQL queries used in analysis
├── visualisations.py           # Python script for all data visualizations
├── email_campaign_data.db      # SQLite database (optional, if sharable)
├── PowerBI/                    # (Optional) Power BI reports
└── README.md                   # Project documentation
