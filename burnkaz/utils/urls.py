from django.urls import path
from .views import ML

urlpatterns = [
    path('ml/', ML.as_view())
]