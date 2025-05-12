from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from encryption import encrypt, decrypt
from schemas import Note, NoteIn, TextRequest
from auth import authenticate_user, create_access_token, get_current_user, users_db
from service import predict_text

app = FastAPI()

# Pydantic models
class EmployeeInput(BaseModel):
    Risk: str
    Working_Hours: int

class EmployeeOutput(BaseModel):
    Risk: str
    Working_Hours: int
    Truth: float
    Indeterminacy: float
    Falsity: float
    Refined_Recommendation: str

# Compute neutrosophic values
def compute_neutrosophic_values(risk: str, working_hours: int):
    risk_truth = {'High': 1.0, 'Moderate': 0.7, 'Low': 0.3}
    T = risk_truth.get(risk, 0.0)

    min_hours = 20
    max_hours = 60
    min_I = 0.1
    max_I = 0.9

    clamped_hours = max(min_hours, min(working_hours, max_hours))
    I = min_I + ((clamped_hours - min_hours) / (max_hours - min_hours)) * (max_I - min_I)
    I = round(I, 2)
    F = round(max(0, 1 - T - I), 2)
    T = round(T, 2)
    return T, I, F

# Get recommendation from file
def get_recommendation_from_file(risk: str, working_hours: int) -> Optional[str]:
    try:
        file_url = 'https://drive.google.com/uc?export=download&id=1i3IjQeLXREZE56ZXEMPna09tGQe9Xxok'
        df = pd.read_excel(file_url)
        row = df[(df['risk'] == risk) & (df['working_hours'] == working_hours)]
        if not row.empty:
            return row.iloc[0]['recommendation']
    except Exception as e:
        print("Error reading Excel file:", e)
    return None

# Refined recommendation logic
def refined_recommendation(T: float, I: float, F: float, base: str):
    if T > 0.7 and F < 0.3:
        return f"URGENT: {base}"
    elif I > 0.6:
        return f"CLARIFY: {base} (High workload uncertainty)"
    return f"NORMAL: {base}"

# API Endpoints
@app.post("/process-employee/", response_model=EmployeeOutput)
async def process_employee(employee: EmployeeInput):
    # Compute neutrosophic values and get recommendation
    T, I, F = compute_neutrosophic_values(employee.Risk, employee.Working_Hours)
    file_recommendation = get_recommendation_from_file(employee.Risk, employee.Working_Hours)

    if not file_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found for given input.")

    # Refine recommendation and return response
    refined = refined_recommendation(T, I, F, file_recommendation)

    return EmployeeOutput(
        Risk=employee.Risk,
        Working_Hours=employee.Working_Hours,
        Truth=T,
        Indeterminacy=I,
        Falsity=F,
        Refined_Recommendation=refined
    )

# Prediction endpoint
@app.post("/predict")
async def predict(request: TextRequest):
    return predict_text(request.text)
