from django.urls import path

from developer.views import DeveloperContacts
from userauth.views import CitiesView
from developer import views
from userauth.views import GetProfile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('developer-profiles', views.DeveloperProfiles, basename='devprofs')
router.register('my-profile', GetProfile, basename='myprof')
router.register('developer-contact', DeveloperContacts, basename='devcontact')
urlpatterns = router.urls
# urlpatterns = [
#     path('developer-profiles/', views.DeveloperProfiles.as_view()),
#     # path('developer-profiles/<int:pk>/', views.DeveloperProfiles.as_view())
# ]


