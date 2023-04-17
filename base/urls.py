from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('signup/', views.userSignup, name='signup'),
    path('logout/', views.userLogout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-password/', views.addPassword, name='add-password'),
    path('edit-password/<str:pk>', views.editPassword, name='edit-password'),
    path('delete-password/<str:pk>/', views.deletePassword, name='delete-password'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('delete-user/', views.deleteUser, name='delete-user'),
]