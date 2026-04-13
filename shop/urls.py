from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('strawberry-chat/', views.strawberry_chat, name='strawberry_chat'),
    path('about/', views.about, name='about'),
    path('price/', views.price, name='price'), 
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),

    # ========== ЖАҢЫ URL'ДЕР (ушул жерге кошобуз) ==========
    path('about/fresh/', views.fresh_view, name='fresh'),
    path('about/callebaut/', views.callebaut_view, name='callebaut'),
    path('about/handmade/', views.handmade_view, name='handmade'),
    path('about/elite/', views.elite_view, name='elite'),
]