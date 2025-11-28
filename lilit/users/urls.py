from django.urls import path

from users.views import RegisterView, VerifyEmail, logout_user, LoginUser, PasswordRecoveryEmail, PasswordRecoveryCode

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('registarate/', RegisterView.as_view(), name='reg'),
    path('registrate/verify/', VerifyEmail.as_view(), name='verify' ),
    path('logout/', logout_user, name='logout'),
    path('recovery/', PasswordRecoveryEmail.as_view(), name='recovery'),
    path('recovery/confirmation', PasswordRecoveryCode.as_view(), name='confirmation'),

]