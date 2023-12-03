from django.urls import path
from accounts import views

urlpatterns = [
	path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
	path('register/telegram', views.sign_up_telegram, name='register_telegram'),
]