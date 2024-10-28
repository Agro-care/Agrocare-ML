from django.urls import path
from . import views


urlpatterns = [
    # Endpoint for crop recommendation predictions
    path('crop-recommendation/predict/', views.crop_recommendation_predict, name='Crop-Recommendation-System-API'),
    # Future endpoints can be added here
]
