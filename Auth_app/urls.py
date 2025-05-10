from django.urls import path,include
from Auth_app import views

urlpatterns = [
    path("Login/",views.signin, name="Login"),
    path("Login/<str:id>",views.verify, name="Verification"),
    path("Google/", views.google, name="GoogleAuth"),
    path("Logout/", views.signout, name="Logout")
]


