from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'shop'   # ← Сунушталат (namespace үчүн)

urlpatterns = [
    path('', views.home, name='home'),
    
    # ==================== АВТОРИЗАЦИЯ ====================
    path('register/', views.register, name='register'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='shop/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # ==================== ПАРОЛЬ КАЛЫБЫНА КЕЛТИРҮҮ ====================
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='shop/password_reset.html'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='shop/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='shop/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='shop/password_reset_complete.html'
    ), name='password_reset_complete'),

    # ==================== БАШКА БЕТТЕР ====================
    path('strawberry-chat/', views.strawberry_chat, name='strawberry_chat'),
    
    path('about/', views.about, name='about'),
    path('price/', views.price, name='price'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),

    path('about/fresh/', views.fresh_view, name='fresh'),
    path('about/callebaut/', views.callebaut_view, name='callebaut'),
    path('about/handmade/', views.handmade_view, name='handmade'),
    path('about/elite/', views.elite_view, name='elite'),
]