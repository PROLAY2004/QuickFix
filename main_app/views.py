from django.shortcuts import render,redirect
from django.conf import settings
from bson import ObjectId
from .models import AdminDetails

userdata = settings.MONGO_DB.userdata
services = settings.MONGO_DB.services

# Create your views here.
def index(request):
    return redirect("Home")


def home(request):
    if(request.session.get('user_id')):
        userid = request.session.get('user_id')
        link = "/Dashboard/" + userid +"/"
        user = userdata.find_one({"_id" : ObjectId(userid)})
        email = user["Email"]
        admin = False
        superAdmin = False
        if (AdminDetails.objects.filter(email = email).exists()):
            admin = True
            if (AdminDetails.objects.get(email = email).is_superAdmin == True):
                superAdmin = True
                
        context = {
            "link": link,
            "id" : userid,
            "Admin" : admin,
            "superAdmin" : superAdmin,
            "services" : services.find()
        }
        return render(request,"home.html",context)
    else:
        context = {
            "services" : services.find(),
            "link" : "/Auth/Login/",
        }
        return render(request,"home.html",context)