from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crop_prediction import predict_crop, create_dataframe

# Constants for error messages
ERROR_MESSAGES = {
    'not_post': 'not using POST request',
    'invalid_content_type': 'Content type must be application/json',
    'invalid_input': 'Invalid input data'
}


# API endpoint for crop recommendation prediction
@csrf_exempt
def crop_recommendation_predict(request: HttpResponse) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['not_post']}, status=400)
    # try catch block to handle IntegrityError
    try:
        # check if content type is application/json
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['invalid_content_type']}, status=400)
        # convert request.body to dataframe format for prediction
        data = request.body
        df = create_dataframe(data)
        # predict crop using predict_crop function
        prediction_result = predict_crop(df)
        # return prediction result as json response
        return JsonResponse({'error': 'false', 'prediction': prediction_result}, status=200)
    except ValueError as ve:
        return JsonResponse({'error': 'true', 'message': ERROR_MESSAGES['invalid_input']}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'true', 'message': str(e)}, status=500)
