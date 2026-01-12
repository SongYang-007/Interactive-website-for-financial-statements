# Interactive-website-for-financial-statements

An interactive financial reporting web application built with Python Dash that converts uploaded raw data into dynamic financial statements and visual analytics, including revenue, profitability, expense, and multi-year performance dashboards.



\# Interactive Financial Statements Web Dashboard



An interactive financial reporting web application built with \*\*Python Dash\*\* that transforms uploaded raw financial data into dynamic, structured financial statements and visual analytics.



The dashboard automatically generates visualizations for \*\*business unit revenue\*\*, \*\*profit margins\*\*, \*\*cumulative revenue\*\*, \*\*expense \*\*, and \*\*five-year performance summaries\*\*, along with interactive \*\*Income Statement\*\*, \*\*P\&L Summary\*\*, and \*\*Balance Sheet Summary\*\* views.



---



**Features**



\- Upload raw financial data (CSV or Excel) and automatically generate interactive dashboards  

\- Visualize \*\*business unit revenue\*\* using stacked bar charts  

\- Analyze \*\*profit margins\*\* with dual-axis (absolute value and percentage) charts  

\- Display \*\*cumulative revenue\*\* using waterfall charts  

\- Track \*\*expense\*\* through stacked area charts  

\- Generate a \*\*five-year performance summary\*\* with key metrics and micro trend charts  

\- Automatically produce \*\*Income Statement\*\*, \*\*P\&L Summary\*\*, and \*\*Balance Sheet Summary\*\* views  

\- Built-in sample dataset when no file is uploaded  



---



 **Tech Stack**



\- Python  

\- Dash  

\- Plotly  

\- Pandas  

\- NumPy  



---



**Data Format**



Uploaded files should include the following required columns:



```text

Year

Business 1

Business 2

Business 3

Consolidated

COGS

Profit Margin ($)

Profit Margin (%)

Salaries and Benefits

Rent and Overhead

Depreciation \& Amortization

Interest

Total Expenses

If a column named Total is detected instead of Total Expenses, the application will automatically rename it.



**Sample Data**



A sample Excel template is provided in the repository:



data/CFI-Excel-Data-Visualization-and-Dashboards-Template.xlsx





This file can be used directly to test the dashboard by uploading it through the web interface.



**How to Run**



Install required dependencies:



pip install dash pandas numpy plotly





Run the Dash application:



python dashboard1.py





Open your browser and visit:



http://127.0.0.1:8050



**Project Structure**

Interactive Financial Statements Web Dashboard/

│

├── dashboard1.py

├── README.md

├── .gitignore

└── data/

&nbsp;   └── CFI-Excel-Data-Visualization-and-Dashboards-Template.xlsx



**Use Case**



This project is suitable for:



Financial performance analysis and reporting



Business analytics and data visualization demonstrations



Academic projects and portfolio showcases



Dash-based interactive web application development



**Notes**



If no file is uploaded, the dashboard will use built-in sample data



Uploaded data is validated before visualization



Designed for clarity, consistency, and financial reporting readability

