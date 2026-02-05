# Supply Chain Control Tower and Resilience Dashboard

## Project Overview
This project simulates a real-world Supply Chain Control Tower designed to monitor supplier performance, delivery reliability, and inventory capital exposure. 

The architecture is a hybrid analytical system: it utilizes a Python-based backend for real-time data validation and ML-driven risk prediction, paired with a comprehensive Power BI dashboard for executive-level business intelligence and root-cause analysis.

## Technology Stack
- **Data Engineering:** Python, FastAPI, and Great Expectations (v1.x) for automated validation.
- **Machine Learning:** Scikit-Learn (Logistic Regression) for predictive risk modeling.
- **Business Intelligence:** Power BI (DAX, Data Modeling) and Excel for scenario simulation.
- **Database Logic:** SQL Server and Pandas for business queries, joins, and aggregations.
- **Data Modeling:** Star Schema design (Fact and Dimension modeling).

## Key Performance Indicators (KPIs)
- **OTIF (On-Time In-Full Percentage):** Implemented via DAX and Python logic to measure delivery reliability.
- **Average Supplier Delay:** Quantifying lead-time variance across the supply base.
- **Net Stock Position:** Real-time monitoring of inventory levels.
- **Inventory Capital Exposure:** Measuring capital tied up in high-value categories.
- **Supplier Risk Score:** ML-driven classification (High/Low Risk) based on historical delay variance.

## Business Insights and Analytics
- **Root Cause Identification:** Designed Decomposition Tree analysis in Power BI to identify suppliers contributing to performance degradation.
- **Operational Resilience:** Quantified resilience using OTIF metrics and delay variance analysis.
- **Financial Optimization:** Measured capital exposure to identify tied-up liquidity in high-value inventory.
- **Interactive Analysis:** Designed multi-dimensional filtering for supplier, location, and category-level insights.

## Project Structure
- `data/`: Automated transaction generation and star schema datasets.
- `pipeline/`: Data quality validation and schema enforcement logic.
- `ml/`: Predictive model training (Logistic Regression) and serialization.
- `api/`: FastAPI endpoints serving real-time KPIs and risk predictions.
- `power_bi/`: Power BI .pbix files containing DAX measures and interactive visualizations.
- `frontend/`: Streamlit dashboard for real-time ML-based interaction.

## Execution Instructions
1. **Clone the repository:**
   git clone https://github.com/YOUR_USERNAME/Supply-Chain-Control-Tower.git
2. **Setup Environment:**
   pip install -r requirements.txt
3. **Data & ML Pipeline:**
   python generate_data.py && python ml/train.py
4. **Launch Backend:**
   uvicorn api.main:app --reload
5. **Analyze Data:**
   Open the .pbix file in the `power_bi/` directory to view the resilience dashboard.