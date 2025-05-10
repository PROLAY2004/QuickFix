from django.urls import path,include
from main_app import views

urlpatterns = [
    path("",views.index, name="Index"),
    path("Home/",views.home, name="Home"),
]
