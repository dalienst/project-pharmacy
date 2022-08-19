from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from users.views import UserRegister, PharmacistCreateView, PharmacistDetailView, PharmacistView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", UserRegister.as_view(), name="register"),
    path("employee/", PharmacistCreateView.as_view(), name="employee"),
    path("employees/", PharmacistView.as_view(), name='all-employees'),
    path("employee/<str:pharmacist>/", PharmacistDetailView.as_view(), name="update-employee")
]