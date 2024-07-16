from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('home/', views.homePage, name='home'),
    path('logout/', views.logoutButton, name = 'logout'),
    path('problems/', views.problemPage, name='problemPage'),
    path('discussions/', views.discussionPage, name='discussionPage'),
    path('problems/<int:id>/', views.solvePage, name='solvePage'),
]
