from django.urls import path    
from . import views
from django.contrib.auth.views import LogoutView

app_name = "account"

urlpatterns = [
<<<<<<< Updated upstream
    path('login/', views.LoginView.as_view(),name='login-view'),    
    path('logout/', LogoutView.as_view(next_page='/'),name='logout-view'),
    path('signup/', views.SignUpView.as_view(),name='signup-view'),
=======
    path("login/", views.LoginView.as_view(), name="login-view"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout-view"),
    path("signup/", views.SignUpView.as_view(), name="signup-view"),
    path("api/v1/", include("accounts.api.v1.urls"), name="api-v1"),
>>>>>>> Stashed changes
]
