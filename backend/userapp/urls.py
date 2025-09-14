from django.urls import path
from userapp.views import *
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
	
	path('email-signup/', EmailSignupView.as_view(), name='email_signup'),
	path('complete-signup/', CompleteSignupView.as_view(), name='complete_signup'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('profile/', UserProfileView.as_view(), name='user_profile'),
	path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
	path('reset-password/', PasswordResetView.as_view(), name='reset_password'),


]