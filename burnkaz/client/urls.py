from django.urls import path
from . import views

urlpatterns = [
    path('incontact/', views.ClientContactDev.as_view(), name='incontact')
]