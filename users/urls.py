from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "users"

urlpatterns = [
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    # Request a password rest
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    # Password rest request sent
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    # Password reset via the sent link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # Change password
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    # Password reset complete
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
