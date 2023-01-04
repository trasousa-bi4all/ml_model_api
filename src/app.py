import os 
import pickle
import pandas as pd
import uvicorn
import logging
from fastapi import FastAPI, status
from pydantic import BaseModel

modelPath = os.getenv("MODELPATH")
logger = logging.getLogger(__name__)
app = FastAPI()


# function to Load trained model
def LoadSerialized_model(modelPath: str):
    # Loading model
    unpackedModel = None
    with open(modelPath,'rb') as infile:
        unpackedModel = pickle.load(infile)
    return unpackedModel

# function to return the model object 
def ScoreModel(model,data):
    aux_dict = {}
    for k,v in data.items():
        aux_dict[k] = [v]
    df = pd.DataFrame.from_dict(aux_dict)
    prediction = model.predict(df)
    return prediction

class ModelFeatures(BaseModel):
    num__Age: float
    num__EnvironmentSatisfaction: float 
    num__JobInvolvement: float
    num__JobLevel: float
    num__JobSatisfaction: float
    num__MonthlyIncome: float
    num__StockOptionLevel: float
    num__TotalWorkingYears: float
    num__YearsAtCompany: float
    num__YearsInCurrentRole: float
    num__YearsWithCurrManager: float
    oneHot__x0_Travel_Frequently: float
    oneHot__x1_Research_and_Development: float
    oneHot__x4_Laboratory_Technician: float
    oneHot__x4_Manager: float
    oneHot__x4_Manufacturing_Director: float
    oneHot__x4_Research_Director: float
    oneHot__x4_Sales_Representative: float
    oneHot__x5_Divorced: float
    oneHot__x5_Married: float
    oneHot__x5_Single: float
    oneHot__x6_No: float
    oneHot__x6_Yes: float

@app.post("/api/Model/", status_code=status.HTTP_200_OK)
def create_model(model: ModelFeatures):
    features_dict = model.dict()
    serializedModel = LoadSerialized_model(modelPath)
    modelScore = ScoreModel(serializedModel, features_dict)
    return str(modelScore[0])

@app.get("/api/", status_code=status.HTTP_200_OK)
def read_root():
    return {"API": "Coimbra"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)