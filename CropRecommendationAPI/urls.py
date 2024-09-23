from django.urls import path
from . import views

urlpatterns = [
    path('crop-recommendation/predict', views.crop_recommendation_predict),
]