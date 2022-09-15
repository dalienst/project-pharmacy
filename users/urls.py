from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from users.views import (
    UserRegister,
    PharmacistCreateView,
    PharmacistDetailView,
    PharmacistView,
    ManufacturerDetailView,
    ManufacturerListView,
    ManufacturerListCreateView,
    CustomerListView,
    CustomerListCreateView,
    CustomerDetailView,
    UserDetailView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", UserRegister.as_view(), name="register"),
    path("me/<str:id>/", UserDetailView.as_view(), name="user-detail"),

    path("employee/", PharmacistCreateView.as_view(), name="employee"),
    path("employees/", PharmacistView.as_view(), name='all-employees'),
    path("employee/<str:pharmacist>/", PharmacistDetailView.as_view(), name="update-employee"),

    path("customer/", CustomerListCreateView.as_view(), name="customer"),
    path("customers/", CustomerListView.as_view(), name='all-customer'),
    path("customer/<str:customer>/", CustomerDetailView.as_view(), name="update-customer"),

    path("distributor/", ManufacturerListCreateView.as_view(), name="distro"),
    path("distributors/", ManufacturerListView.as_view(), name='all-distros'),
    path("distributor/<str:id>/", ManufacturerDetailView.as_view(), name="update-distro"),

]
