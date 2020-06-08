from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Functions
    path('upload_hws/', views.upload_hws, name="upload_hws"),
    path('contact/', views.contact, name="contact"),

    # Auth
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
