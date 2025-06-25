from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('prediction/', views.prediction, name='prediction'),
    path('hospitals/', views.map_view, name='map_view'),  # ✅ Renamed to match {% url 'map_view' %}
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]
