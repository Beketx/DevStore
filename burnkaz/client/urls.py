from django.urls import path

from developer.views import FeedbackAPIView
from devutils.views import AddFavorite
from . import views

urlpatterns = [
    path('incontact/', views.ClientContactDev.as_view(), name='incontact'),
    path('favorites/', AddFavorite.as_view(), name='incontact'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback')
]