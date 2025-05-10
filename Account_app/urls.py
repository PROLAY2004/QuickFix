from django.urls import path,include
from Account_app import views

urlpatterns = [
    path("<str:userid>/",views.dashboard, name="Account"),
    path('Location/Add/New/<str:userid>/', views.location, name='location'),
    path('Location/Delete/<int:index>/<str:userid>/', views.delAddr, name='Delete_Location'),
    path('Location/Edit/<int:index>/<str:userid>/', views.editAddr, name='Edit_Location'),
    path('Location/Set/Default/<int:index>/<str:userid>/', views.setDefault, name='Default_Location'),
    path('Orders/<str:userid>/', views.orders, name='Orders'),
    path('Appointment/<str:userid>/', views.slots, name='Book_Slot'),
    path('Appointment/Cancel/<str:userid>/<str:appointmentid>/', views.delAppointment, name='Delete Appointment'),
    path('Settings/<str:userid>/', views.setting, name='Settings'),
]
