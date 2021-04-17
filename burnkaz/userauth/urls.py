from django.urls import re_path, include, path

from rest_framework.routers import DefaultRouter
from .views import RegistrationStepOne, RegistrationStepTwo, RegistrationStepThree, \
    RegistrationStepFour, RegistrationStepFive, CitiesView
from .views import LoginAPIView, ValidateOTP, ValidatePhoneSendOTP



urlpatterns = [
    re_path(r'^registration/step/1?$', RegistrationStepOne.as_view(), name='user_registration_1'),
    re_path(r'^registration/step/2?$', RegistrationStepTwo.as_view(), name='user_registration_2'),
    re_path(r'^registration/step/3?$', RegistrationStepThree.as_view(), name='user_registration_3'),
    re_path(r'^registration/step/4?$', RegistrationStepFour.as_view(), name='user_registration_4'),
    re_path(r'^registration/step/5?$', RegistrationStepFive.as_view(), name='user_registration_5'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    path('send-otp/', ValidatePhoneSendOTP.as_view()),
    path('validate-otp/', ValidateOTP.as_view())

]
