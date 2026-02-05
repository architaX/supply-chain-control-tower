import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
import os
import sys

def train_risk_model():
    print("--- Starting Training Process ---")
    
    # 1. Ensure the directory exists
    if not os.path.exists('ml'):
        print("Creating 'ml' directory...")
        os.makedirs('ml')
    
    # 2. Check if data exists
    data_path = "data/Transactions.csv"
    if not os.path.exists(data_path):
        print(f"❌ ERROR: {data_path} not found! Run generate_data.py first.")
        return

    # 3. Load and process data
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    purchases = df[df['Type'] == 'Purchase'].copy()
    if purchases.empty:
        print("❌ ERROR: No purchase data found in Transactions.csv.")
        return

    print(f"Found {len(purchases)} purchase records. Feature engineering...")
    
    # Aggregate stats per supplier
    supplier_stats = purchases.groupby('SupplierID').agg({
        'Actual_Delivery_Days': 'mean',
        'Promised_Delivery_Days': 'mean',
        'Quantity': 'mean'
    }).reset_index()
    
    # Create target variable
    supplier_stats['avg_delay'] = supplier_stats['Actual_Delivery_Days'] - supplier_stats['Promised_Delivery_Days']
    supplier_stats['is_high_risk'] = (supplier_stats['avg_delay'] > 3).astype(int)
    
    X = supplier_stats[['Actual_Delivery_Days', 'Promised_Delivery_Days', 'Quantity']]
    y = supplier_stats['is_high_risk']
    
    # 4. Train the model
    print("Fitting Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X, y)
    
    # 5. Save the model
    model_filename = 'ml/model.joblib'
    print(f"Attempting to save model to: {os.path.abspath(model_filename)}")
    
    try:
        joblib.dump(model, model_filename)
        if os.path.exists(model_filename):
            print(f"✅ SUCCESS: {model_filename} generated! Size: {os.path.getsize(model_filename)} bytes")
        else:
            print("❌ ERROR: joblib.dump ran but file is missing.")
    except Exception as e:
        print(f"❌ FATAL ERROR during save: {e}")

if __name__ == "__main__":
    train_risk_model()