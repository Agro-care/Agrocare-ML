from django.urls import path, include
from . import views

urlpatterns = [
    path('FRS/predict/', views.predictor, name="Predictor"),
    # path('predict', views.formData, name="Formdata"),
]