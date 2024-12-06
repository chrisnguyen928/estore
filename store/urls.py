from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_item/', views.update_item, name = 'update_item'),
    path('checkout/process_order/', views.process_order, name = 'process_order'),
    path('about/', views.about, name = 'about'),
    path('register/',views.register, name = 'register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'store/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'store/logout.html'), name = 'logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'store/password_reset.html'), name = 'password_reset'),
    path('password-reset-done/', auth_views.PasswordResetView.as_view(template_name = 'store/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'store/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'store/password_reset_complete.html'), name = 'password_reset_complete'),
]