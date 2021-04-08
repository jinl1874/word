from django.urls import path
from home import views


urlpatterns = [
    path('', views.index),
    path('index/', views.index),
]