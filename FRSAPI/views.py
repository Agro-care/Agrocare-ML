from django.shortcuts import render
from joblib import load
from django.http import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from GoogleTrans.google_translate import translate_text, get_dest

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
def fertilizer_recommendation_predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            dest_language = get_dest(request.body)
            # print(dest_language)
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
            if dest_language is None or dest_language == 'en':
                translated_result = result
            else:
                translated_result = translate_text(result, dest_language)
            return JsonResponse({"Prediction": translated_result})
        except ValueError as ve:
            return JsonResponse({'error': 'true', 'message': f"{ERROR_MESSAGES['invalid_input']} {ve}"}, status=400)
        except Exception as e:
            return JsonResponse({'error':str(e)+"error"})

    return render(request,"main.html")
