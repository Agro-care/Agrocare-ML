from django.shortcuts import render
# from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from django.forms.models import model_to_dict

# Create your views here.
@csrf_exempt
def crop_recommendation_predict(request):
    if request.method != "POST":
        return JsonResponse({'error': 'true', 'message': 'not using POST request'}, status=400)
    data = json.loads(request.body)
    N = data.get('Nitrogen')
    P = data.get('Phosphorous')
    K = data.get('Potassium')
    temperature = data.get('Temperature')
    humidity = data.get('Humidity')
    ph = data.get("Ph")
    rainfall = data.get("Rainfall")
    input_data = [[N, P, K, temperature, humidity, ph, rainfall]]