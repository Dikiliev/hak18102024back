from django.urls import include, path
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views
from .views import UserProfileView, UserViewSet

router = routers.DefaultRouter()
router.register(r'list', UserViewSet, basename='products')

urlpatterns = [
    path('', views.get_routes),
    path('', include(router.urls)),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),
]