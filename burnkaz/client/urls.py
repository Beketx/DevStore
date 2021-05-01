from django.urls import path

from devutils.views import AddFavorite
from . import views

urlpatterns = [
    path('incontact/', views.ClientContactDev.as_view(), name='incontact'),
    path('favorites/', AddFavorite.as_view(), name='incontact')
]