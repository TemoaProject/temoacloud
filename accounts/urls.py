from django.conf.urls import url
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.registration_view, name='register'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
