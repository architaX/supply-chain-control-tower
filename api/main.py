from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
import os

app = FastAPI(title="Supply Chain Control Tower API")

# Configuration
DATA_PATH = "data/Transactions.csv"
MODEL_PATH = "ml/model.joblib"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Transaction data not found. Run generate_data.py.")
    return pd.read_csv(DATA_PATH)

@app.get("/")
def home():
    """Root endpoint to verify API status."""
    return {
        "project": "Supply Chain Control Tower",
        "status": "Online",
        "documentation": "/docs",
        "metrics_available": ["/otif", "/avg-delay", "/supplier-risk/{id}"]
    }

@app.get("/otif")
def get_otif():
    """Calculates On-Time In-Full (OTIF) % for all purchases."""
    df = load_data()
    purchases = df[df['Type'] == 'Purchase']
    if purchases.empty:
        return {"metric": "OTIF", "value": "0%", "note": "No purchases found"}
    
    on_time = purchases[purchases['Actual_Delivery_Days'] <= purchases['Promised_Delivery_Days']]
    score = (len(on_time) / len(purchases)) * 100
    return {"metric": "OTIF", "value": f"{score:.2f}%"}

@app.get("/avg-delay")
def get_delay():
    """Calculates the average delivery time for purchases."""
    df = load_data()
    avg = df[df['Type'] == 'Purchase']['Actual_Delivery_Days'].mean()
    return {"metric": "Average Delivery Days", "value": round(avg, 2) if not pd.isna(avg) else 0}

@app.get("/supplier-risk/{supplier_id}")
def predict_risk(supplier_id: int):
    """Predicts risk for a specific supplier using the trained ML model."""
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Model not trained. Run ml/train.py first.")
    
    # Load model and data
    model = joblib.load(MODEL_PATH)
    df = load_data()
    
    # Filter history for this specific supplier
    sup_data = df[(df['SupplierID'] == supplier_id) & (df['Type'] == 'Purchase')]
    if sup_data.empty:
        raise HTTPException(status_code=404, detail=f"No purchase history found for Supplier ID {supplier_id}")
    
    # Prepare features (Must match the 3 features used during training)
    avg_actual = sup_data['Actual_Delivery_Days'].mean()
    avg_promised = sup_data['Promised_Delivery_Days'].mean()
    avg_qty = sup_data['Quantity'].mean()

    # Create a DataFrame to include feature names (fixes UserWarning)
    features = pd.DataFrame(
        [[avg_actual, avg_promised, avg_qty]], 
        columns=['Actual_Delivery_Days', 'Promised_Delivery_Days', 'Quantity']
    )
    
    # Predict
    prediction = model.predict(features)[0]
    return {
        "supplier_id": supplier_id, 
        "risk_assessment": "High Risk" if prediction == 1 else "Low Risk",
        "stats": {
            "avg_actual_days": round(avg_actual, 2),
            "avg_promised_days": round(avg_promised, 2),
            "avg_quantity": round(avg_qty, 2)
        }
    }