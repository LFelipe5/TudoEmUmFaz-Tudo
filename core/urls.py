from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:pk>/<str:action>/', views.task_action, name='task-action'),
    path('scraper/', views.scraper, name='scraper'),
]
