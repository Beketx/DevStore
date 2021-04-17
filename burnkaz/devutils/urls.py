from rest_framework.routers import DefaultRouter

from userauth.views import CitiesView
from .views import SkillsView, StacksView

router = DefaultRouter()


router.register("skills", SkillsView, basename="skills")
router.register("stacks", StacksView, basename="stacks")
router.register("cities", CitiesView, basename="cities")

urlpatterns = router.urls
