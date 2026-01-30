# Supply Chain Control Tower & Resilience Dashboard

## **Project Overview**

This project simulates a Supply Chain Control Tower to analyze supplier performance, delivery reliability, and inventory position.

The solution was built using a structured workflow:

- Created realistic supply chain datasets in Excel  
- Performed business analysis using SQL Server  
- Built a star schema data model in Power BI  
- Developed KPIs using DAX  
- Designed an executive dashboard for performance monitoring  

---

## **Technology Used**

### **SQL Server**
- Joins between fact and dimension tables  
- Aggregations and grouped analysis  
- Delivery delay and stock calculations  

### **Power BI**
- One-to-many relationship modeling  
- DAX measures for KPI calculation  
- Interactive dashboard design  

### **Excel**
- Dataset creation  
- Scenario simulation (late suppliers and stock imbalances)  

---

## **Key KPIs Implemented**

- **OTIF (On-Time-In-Full Percentage)**
- **Average Supplier Delivery Delay**
- **Net Stock Position (Purchases – Sales)**
- **Inventory Value by Category**
- **Purchase vs Sales Transaction Count**

---

## **Business Analysis Performed**

- Identified suppliers with high average delivery delays  
- Calculated OTIF to measure delivery reliability  
- Analyzed inventory exposure by product category  
- Detected negative stock situations to simulate stockout risk  
- Used decomposition tree to break down OTIF by supplier and category  
