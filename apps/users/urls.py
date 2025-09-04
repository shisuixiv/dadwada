from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import RegisterView,LoginView,ProfileView,UserViewSet

router = DefaultRouter()
router.register("users",UserViewSet,basename="users")


urlpatterns = [
    path("register", RegisterView.as_view(),name="register"),
    path("login", LoginView.as_view(),name="login"),
    path("profile", ProfileView.as_view(),name="profile"),

]