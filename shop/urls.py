from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Дарек бул жерде 'strawberry-chat/' болушу шарт
    path('strawberry-chat/', views.strawberry_chat, name='strawberry_chat'),
    path('about/', views.about, name='about'),
    path('price/', views.price, name='price'), 
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),
]