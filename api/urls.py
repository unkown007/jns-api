from django.urls import path, include
from user.views import AuthCodeView, AuthCodeValidateView, ObtainTokenView, AuthUserEmailView

urlpatterns = [
    path('auth/', ObtainTokenView.as_view()),
    path('auth/code/', AuthCodeView.as_view()),
    path('auth/code/validate/', AuthCodeValidateView.as_view()),
    path('auth/email/', AuthUserEmailView.as_view()),
    path('user/', include('user.urls')),
]
