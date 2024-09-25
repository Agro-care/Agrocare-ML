from django.urls import path
from . import views


urlpatterns = [
    # Endpoint for crop recommendation predictions
    path('crop-recommendation/predict/', views.crop_recommendation_predict, name='crop_recommendation_predict'),
    # Future endpoints can be added here
]
