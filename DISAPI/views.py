from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from DISAPI.disease_prediction import predict_disease
# Constants for error messages
ERROR_MESSAGES = {
    'not_post': 'not using POST request',
    'invalid_content_type': 'Content type must be application/json',
    'invalid_input': 'Invalid input data',
    'no_photo': 'Photo is required'
}


# API endpoint for disease identification prediction
@csrf_exempt
def disease_identification_predict(request: HttpResponse) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['not_post']}, status=400)
    # try catch block to handle IntegrityError
    try:
        # check if content type is application/json
        if request.content_type != 'multipart/form-data':
            return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['invalid_content_type']}, status=400)
        # convert request.body to dataframe format for prediction
        photo = request.FILES.get('file')
        # check if picture is not empty
        if not photo:
            return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['no_photo']}, status=400)
        # predict disease using predict_disease function
        prediction_result = predict_disease(photo)
        # return prediction result as json response
        return JsonResponse({'error': 'false', 'prediction': prediction_result}, status=200)
    except ValueError as ve:
        return JsonResponse({'error': 'true', 'message': f"{ERROR_MESSAGES['invalid_input']} {ve}"}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'true', 'message': str(e)}, status=500)
