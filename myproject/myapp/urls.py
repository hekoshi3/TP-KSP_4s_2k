from django.urls import path
from . import views

urlpatterns = [
    path('sdgen/', views.image_generation_view, name='image_generation'),
    path('register/', views.register, name='register'),
]
