from django.shortcuts import render
from joblib import load
from django.http import JsonResponse
import pandas as pd
import json

model = load("./MLmodels/fertilizer.joblib")
sencoder = load("./MLmodels/soil_encoder.joblib")
cencoder = load("./MLmodels/crop_encoder.joblib")
fencoder = load("./MLmodels/fer_encoder.joblib")

def predictor(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recieved = data["data"]
            temp = int(recieved['temperature'])
            soil = recieved["soil"]
            crop = recieved["crop"]
            humid = int(recieved["humidity"])
            moisture = int(recieved["moisture"])
            nitrogen = int(recieved["nitrogen"])
            pot = int(recieved["potassium"])
            phos = int(recieved["phosphorous"])
            # print(temp, humid, crop)
            s=sencoder.transform([soil])[0]
            c=cencoder.transform([crop])[0]
            inputData = pd.DataFrame(
                {
                    "Temparature" : [temp],
                    "Humidity" : [humid],
                    "Soil Moisture": [moisture],
                    "Soil Type": [s],
                    "Crop Type" : [c],
                    "Nitrogen" : [nitrogen],
                    "Potassium" : [pot],
                    "Phosphorous" : [phos]
                }
            )
            # print(inputData)
            prediction = model.predict(inputData)
            # print(prediction)
            result = fencoder.inverse_transform(prediction)[0]
            return JsonResponse({"Prediction":result})
        except Exception as e:
            return JsonResponse({'error':str(e)})


    return render(request,"main.html")