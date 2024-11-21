from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from CRSAPI.crop_prediction import predict_crop, create_dataframe
from GoogleTrans.google_translate import translate_text, get_dest
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
        print(data)
        df = create_dataframe(data)
        dest_language = get_dest(data)
        # predict crop using predict_crop function
        prediction_result = predict_crop(df)
        if dest_language is None or dest_language == 'en':
            translated_result = prediction_result
        else:
            translated_result = translate_text(prediction_result, dest_language)
        # return prediction result as json response
        return JsonResponse({'error': 'false', 'prediction': translated_result}, status=200)
    except ValueError as ve:
        return JsonResponse({'error': 'true', 'message': f"{ERROR_MESSAGES['invalid_input']} {ve}"}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'true', 'message': str(e)}, status=500)
