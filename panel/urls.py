from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel, name='panel'),

    # Groups
    path('groups/', views.groups, name='groups'),
    path('groups_add/', views.groups_add, name='groups_add'),
    path('groups_edit/<int:id>/', views.groups_edit, name='groups_edit'),
    path('groups_delete/<int:id>/', views.groups_delete, name='groups_delete'),

    # Students
    path('students/', views.students, name='students'),
    path('students_add/', views.students_add, name='students_add'),
    path('students_edit/<int:id>/', views.students_edit, name='students_edit'),
    path('students_delete/<int:id>/', views.students_delete, name='students_delete'),

    # Lessons
    path('lessons/', views.lessons, name='lessons'),
    path('lessons_add/', views.lessons_add, name='lessons_add'),
    path('lessons_delete/<int:id>/', views.lessons_delete, name='lessons_delete'),

    # Clients
    path('clients/', views.clients, name='clients'),
    path('clients_complete/<int:id>/', views.clients_complete, name='clients_complete'),

    # Home works
    path('hws/', views.hws, name='hws'),
    path('hws_delete/<int:id>/', views.hws_delete, name='hws_delete'),
    path('hws_complete/<int:id>/', views.hws_complete, name='hws_complete'),

    # Download files
    path('download/<int:id>/', views.download, name="download"),
    path('download_hws/<int:id>/', views.download_hws, name="download_hws"),
]
