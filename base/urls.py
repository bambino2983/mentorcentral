from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('kb/<str:pk>/', views.kb, name="kb"),
    path('create-kb/', views.createKb, name="create-kb"),
    path('update-kb/<str:pk>/', views.updateKb, name="update-kb"),
    path('delete-kb/<str:pk>/', views.deleteKb, name="delete-kb"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]