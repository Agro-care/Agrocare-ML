from django.urls import path
from . import views

urlpatterns = [
    path('DIS/predict/', views.disease_identification_predict, name="Disease-Identification-System-API"),
]