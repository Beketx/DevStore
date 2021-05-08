from django.urls import path

from developer.views import DeveloperContacts
from devutils.views import MyFavorites
from userauth.views import CitiesView
from developer import views
from userauth.views import GetProfile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('developer-profiles', views.DeveloperProfiles, basename='devprofs')
router.register('my-profile', GetProfile, basename='myprof')

router.register('developer-contact', DeveloperContacts, basename='devcontact')
router.register('review', views.ReviewView, basename='review')
router.register('rating', views.RatingView, basename='rating')
# router.register('feedback', views.FeedbackAPIView, basename='review-rating')
urlpatterns = router.urls



