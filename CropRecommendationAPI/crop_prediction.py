import joblib
from pathlib import Path
import pandas as pd
import json


# function to predict the crop based on the input data
# input: json data containing the crop parameters
# output: predicted crop name
def predict_crop(data: pd.DataFrame) -> str:
    # get the path of the model file
    # /root/Agrocare-ML/MLModels/crop_recommendation_random_forest.joblib
    model_path = "/root/Agrocare-ML/MLModels/crop_recommendation_random_forest.joblib"

    # load the model
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise FileNotFoundError("Model file not found.")

    # predict the crop
    prediction = model.predict(data)[0]

    # return the predicted crop
    return prediction


# function to create a pandas dataframe from the input json data
# input: json data containing the crop parameters
# output: pandas dataframe containing the crop parameters
def create_dataframe(json_data: str) -> pd.DataFrame:
    # convert data to pandas dataframe
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data.")

    required_fields = ['Nitrogen', 'Phosphorous', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall']

    # check if all required fields are present in the data
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # create the pandas dataframe
    df = pd.DataFrame({
        'N': [float(data.get('Nitrogen'))],
        'P': [float(data.get('Phosphorous'))],
        'K': [float(data.get('Potassium'))],
        'temperature': [float(data.get('Temperature'))],
        'humidity': [float(data.get('Humidity'))],
        'ph': [float(data.get("Ph"))],
        'rainfall': [float(data.get("Rainfall"))]
    })
    return df
