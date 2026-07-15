💾 Ultimate Memory Shortage Crisis Dashboard

An interactive data visualization dashboard built with Python, Streamlit, Pandas, and Plotly to analyze the impact of a simulated global RAM memory shortage. The project explores pricing trends, memory specifications, supply chain indicators, and market behavior through interactive charts and filters.

📌 About the Project

The global memory industry has experienced periods of supply shortages, leading to price increases and changing market demand. This project uses a simulated dataset of 10,000 RAM kits to understand how different factors such as brand, memory generation, speed, capacity, and region affect pricing during a shortage.
Instead of presenting raw data, the dashboard transforms the dataset into meaningful visualizations that help users identify market trends and compare products with ease.

🎯 Project Objectives

-> Analyze RAM pricing trends across different brands.
-> Compare DDR4, DDR5, and DDR6 memory generations.
-> Study the relationship between memory capacity, speed, and price.
-> Monitor price changes over time.
-> Explore how market segments influence product pricing.
-> Provide an interactive dashboard for quick and easy analysis.

✨ Features

-> Interactive Streamlit dashboard
-> Dynamic sidebar filters
-> Executive summary section
-> Dataset overview and statistical analysis
-> Missing value analysis
-> Sample dataset preview
-> Interactive Plotly visualizations
-> Real-time dashboard metrics
-> Business insights generated from every chart
-> Final project summary with key findings

📊 Dashboard Visualizations

The dashboard includes multiple interactive charts such as:
-> Average RAM Price by Brand
-> Memory Capacity Distribution
-> Price vs Capacity Scatter Plot
-> Monthly Price Trend
-> Price Distribution by Brand (Box Plot)
-> RAM Generation Distribution (Donut Chart)
-> Brand and Model Treemap
-> Recommended Usage Sunburst Chart
-> Speed vs Price Analysis
-> Capacity Distribution by Brand (Violin Plot)

Each visualization includes a short explanation to help users understand the results.

🛠️ Technologies Used

-> Python
-> Streamlit
-> Pandas
-> NumPy
-> Plotly Express

📂 Dataset

The project uses a simulated dataset named:

Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv

The dataset contains information such as:

-> Brand
-> Model Name
-> RAM Generation
-> Capacity
-> Speed
-> CAS Latency
-> Voltage
-> Region
-> Market Segment
-> Price
-> Inventory Levels
-> Recommended Usage
-> Supply Chain Indicators

🚀 Installation

Clone the repository:
git clone https://github.com/your-username/your-repository.git
Move into the project folder:
cd your-repository
Install the required libraries:
pip install -r requirements.txt
Run the Streamlit application:
streamlit run Hardware.py

📁 Project Structure

├── Hardware.py
├── Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv
├── requirements.txt
└── README.md

📈 Key Insights

Some of the important findings from the analysis include:

-> Premium RAM brands generally maintain higher average prices.
-> Larger memory capacities usually cost more, especially in enterprise and AI-focused products.
-> Higher memory speeds are often associated with increased pricing.
-> DDR5 dominates the market, while DDR6 appears as an emerging technology.
-> Supply shortages have a noticeable impact on overall RAM prices across different regions.

💡 Future Improvements

Some features that could be added in future versions include:
-> Machine learning models for price prediction.
-> Sales forecasting.
-> Inventory optimization analysis.
-> Additional KPI dashboards.
-> User authentication and report export options.
-> Live market data integration.

👨‍💻 Author

Developed as a data visualization and analytics project using Python and Streamlit to demonstrate interactive dashboard development and market trend analysis.

📜 License

This project is intended for educational and learning purposes. Feel free to modify and improve it for your own projects.   