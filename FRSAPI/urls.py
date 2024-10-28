from django.urls import path
from . import views

urlpatterns = [
    path('FRS/predict/', views.fertilizer_recommendation_predict, name="Fertilize-Recommendation-System-API"),
]