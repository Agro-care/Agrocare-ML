from django.shortcuts import render
from joblib import load
from django.http import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt

model = load("/root/Agrocare-ML/MLModels/fertilizer.joblib")
sencoder = load("/root/Agrocare-ML/MLModels/soil_encoder.joblib")
cencoder = load("/root/Agrocare-ML/MLModels/crop_encoder.joblib")
fencoder = load("/root/Agrocare-ML/MLModels/fer_encoder.joblib")

ERROR_MESSAGES = {
    'not_post': 'not using POST request',
    'invalid_content_type': 'Content type must be application/json',
    'invalid_input': 'Invalid input data'
}

@csrf_exempt
def predictor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
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
        except ValueError as ve:
            return JsonResponse({'error': 'true', 'message': f"{ERROR_MESSAGES['invalid_input']} {ve}"}, status=400)
        except Exception as e:
            return JsonResponse({'error':str(e)})


    return render(request,"main.html")
