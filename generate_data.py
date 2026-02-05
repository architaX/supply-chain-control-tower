import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def generate_production_data():
    # 1. Suppliers
    suppliers_data = {
        'SupplierID': range(1, 11),
        'SupplierName': [f"Supplier {chr(65+i)}" for i in range(10)],
        'Location': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Surat', 'Jaipur'],
        'PaymentTerms': ['Net 30', 'Net 45', 'Net 60'] * 3 + ['Net 30']
    }
    df_suppliers = pd.DataFrame(suppliers_data)

    # 2. Products
    products_data = {
        'ProductID': range(101, 121),
        'ProductName': [f"Product {i}" for i in range(101, 121)],
        'Category': ['Electronics', 'Raw Material', 'Components', 'Packaging'] * 5,
        'UnitCost': [random.randint(10, 500) for _ in range(20)],
        'MinStockLevel': [random.randint(50, 200) for _ in range(20)]
    }
    df_products = pd.DataFrame(products_data)

    # 3. Transactions (1000 Rows)
    transactions = []
    start_date = datetime(2025, 1, 1)

    for i in range(1, 1001):
        t_type = random.choice(['Purchase', 'Sale'])
        p_id = random.choice(df_products['ProductID'].tolist())
        qty = random.randint(10, 500)
        date = start_date + timedelta(days=random.randint(0, 365))
        
        if t_type == 'Purchase':
            s_id = random.randint(1, 10)
            promised = random.randint(3, 10)
            
            # Synthetic Bias for ML: Supplier 3 and 7 are "High Risk" (Late)
            if s_id in [3, 7]:
                actual = promised + random.randint(4, 10) # Always late
            else:
                actual = promised + random.randint(-2, 1) # Mostly on time
                actual = max(1, actual)
        else:
            # For Sales, we use 0 instead of Null to satisfy Great Expectations
            s_id = 0 
            promised = 0
            actual = 0
            
        transactions.append([
            i, date.strftime('%Y-%m-%d'), p_id, t_type, s_id, qty, promised, actual
        ])

    df_transactions = pd.DataFrame(transactions, columns=[
        'TransactionID', 'Date', 'ProductID', 'Type', 'SupplierID', 'Quantity', 
        'Promised_Delivery_Days', 'Actual_Delivery_Days'
    ])

    # Save to data folder
    df_suppliers.to_csv('data/Suppliers.csv', index=False)
    df_products.to_csv('data/Products.csv', index=False)
    df_transactions.to_csv('data/Transactions.csv', index=False)
    
    print(f"Successfully generated 1000 transactions in /data folder.")

if __name__ == "__main__":
    generate_production_data()