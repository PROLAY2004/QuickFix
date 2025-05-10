from django.urls import path,include
from Admin_app import views

urlpatterns = [
    path("<str:id>/",views.admin, name="Admin_Dashboard"),
    path("Profile/<str:id>/",views.profile, name="Admin_Profile"),
    path("Services/<str:id>/",views.service, name="Service"),
    path("Services/Edit/<str:id>/<str:serviceid>/",views.editservice, name="Edit_Service"),
    path("Services/Delete/<str:id>/<str:serviceid>/",views.delservice, name="Delete_Service"),
    path("Services/Publish/<str:id>/<str:serviceid>/",views.publish, name="Publish_Service"),
    path("Appointments/<str:id>/",views.appointment, name="Manage_Appointments"),
    path("Appointments/Map/<str:id>/<str:aid>/",views.mapViewer, name="Show_Location"),
    path("Appointments/Cancel/<str:id>/<str:aid>/",views.cancelAppointment, name="Cancel_Appointment"),
]
