from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Functions
    path('delete_self_hws/<int:id>/', views.delete_self_hws, name="delete_self_hws"),
    path('upload_hws/', views.upload_hws, name="upload_hws"),
    path('contact/', views.contact, name="contact"),

    # Auth
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
