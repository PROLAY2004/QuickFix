from django.shortcuts import render,redirect
from django.conf import settings
from bson import ObjectId
from Account_app.models import dp
from main_app.models import AdminDetails
from datetime import datetime,timedelta, time
from django.utils import timezone
import ast

userdata = settings.MONGO_DB.userdata
services = settings.MONGO_DB.services
admin_settings = settings.MONGO_DB.admin_settings
appointments = settings.MONGO_DB.appointments
blocked_slots = settings.MONGO_DB.blocked_slots

# Create your views here.
def admin(request,id):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    
    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]

    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")

    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    # n = services.find().count()
    # print(n)
    context = {
        "Image" : image,
        "id" : id
    }
    return render(request,'Admin/admin_dashboard.html',context)

# Admin Profile
def profile(request,id):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    
    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]

    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")

    if request.method == 'POST':
        name = request.POST.get("username")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        img = request.FILES.get("image")

        update_data = {}
        
        # Build update dictionary based on provided fields
        if name:
            update_data["Name"] = name
        if gender:
            update_data["Gender"] = gender
        if dob:
            update_data["DOB"] = dob

        # Update MongoDB user data if any fields were provided
        if update_data:
            userdata.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )

        # Handle profile picture upload if provided
        if img:
            try:
                profile = dp.objects.get(email=user["Email"])
                if profile.profilepic:
                    profile.profilepic.delete()  # Delete old image
                profile.profilepic = img
                profile.save()
            except dp.DoesNotExist:
                dp.objects.create(email=user["Email"], profilepic=img)

        return redirect(f"/Admin/Custom/Profile/{id}/")
    
    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    context = {
        "Image" : image,
        "id" : id,
        "admin" : AdminDetails.objects.get(email = email),
        "user": user,
    }
    return render(request,'Admin/admin_profile.html',context)



#main service page
def service(request,id):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]

    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")

    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    if request.method == "POST":
        service_name = request.POST.get("service_name")
        service_category = request.POST.get("service_category")
        service_description = request.POST.get("service_description")
        service_image = request.POST.get("service_image")
        admin_name = request.POST.get("admin_name")

        if services.find_one({ "Name" : service_name.capitalize().strip()}):
            processed_services = []
            for s in services.find():
                s["id"] = str(s["_id"])  # Add 'id' field
                processed_services.append(s)

            context = {
                "Image" : image,
                "id" : id,
                "admin_name" : AdminDetails.objects.get(email = email).name,
                "msg" : "Service Already Registered.",
                "services": processed_services,
            }                
            return render(request,"Admin/services.html",context)
        else:
            services.insert_one({
                "Name" : service_name.strip().capitalize(),
                "Category" : service_category,
                "Description" : service_description,
                "Image_URL" : service_image,
                "Added_by" : admin_name,
                "Status" : "Inactive",
                "Time" : datetime.now()
            })
            return redirect(f"/Admin/Custom/Services/{id}/")
        
    processed_services = []
    for s in services.find():
        s["id"] = str(s["_id"])
        processed_services.append(s)

    context = {
        "Image" : image,
        "id" : id,
        "admin_name" : AdminDetails.objects.get(email = email).name,
        "services": processed_services,
    }
    return render(request,'Admin/services.html',context)


#Edit Service
def editservice(request,id,serviceid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]
    thisservice = services.find_one({"_id" : ObjectId(serviceid)})
    
    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")
    
    if not thisservice:
        return redirect(f"/Admin/Custom/Services/{id}/")

    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    if request.method == "POST":
        service_name = request.POST.get("service_name")
        service_category = request.POST.get("service_category")
        service_description = request.POST.get("service_description")
        service_image = request.POST.get("service_image")
        admin_name = request.POST.get("admin_name")

        if services.find_one({ "Name" : service_name.capitalize().strip()}):                                   
            if thisservice["Name"] == service_name.capitalize().strip():
                services.update_one(
                    {"_id" : ObjectId(serviceid)},
                    {"$set" : {
                    "Name" : service_name.strip().capitalize(),
                    "Category" : service_category,
                    "Description" : service_description,
                    "Image_URL" : service_image,
                    "Added_by" : admin_name,
                    "Time" : datetime.now()
                }})
                return redirect(f"/Admin/Custom/Services/{id}/")
            else:
                context = {
                    "id" : id,
                    "admin_name" : AdminDetails.objects.get(email = email).name,
                    "msg" : "Service Already Registered.",
                    "service" : services.find_one({"_id" : ObjectId(serviceid)})
                }                
                return render(request,"Admin/edit_service.html",context)
        else:
            services.update_one(
                {"_id" : ObjectId(serviceid)},
                {"$set" : {
                "Name" : service_name.strip().capitalize(),
                "Category" : service_category,
                "Description" : service_description,
                "Image_URL" : service_image,
                "Added_by" : admin_name,
                "Time" : datetime.now()
            }})
            return redirect(f"/Admin/Custom/Services/{id}/")
            

    context = {
        "Image" : image,
        "id" : id,
        "admin_name" : AdminDetails.objects.get(email = email).name,
        "service" : services.find_one({"_id" : ObjectId(serviceid)})
    }
    return render(request,'Admin/edit_service.html',context)



#delete Service
def delservice(request,id,serviceid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]

    thisservice = services.find_one({"_id" : ObjectId(serviceid)})
    if not thisservice:
        return redirect(f"/Admin/Custom/Services/{id}/")

    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")

    services.delete_one({"_id" : ObjectId(serviceid)})

    return redirect(f"/Admin/Custom/Services/{id}/")


#Publish Service
def publish(request,id,serviceid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id":ObjectId(id)})
    email = user["Email"]

    thisservice = services.find_one({"_id" : ObjectId(serviceid)})
    if not thisservice:
        return redirect(f"/Admin/Custom/Services/{id}/")
    
    if not AdminDetails.objects.filter(email = email).exists():
        return redirect("/Home/")

    if thisservice["Status"] == "Inactive":
        services.update_one({"_id": ObjectId(serviceid)}, {"$set": {"Status": "Active"}})
    elif thisservice["Status"] == "Active":
        services.update_one({"_id": ObjectId(serviceid)}, {"$set": {"Status": "Inactive"}})
    
    return redirect(f"/Admin/Custom/Services/{id}/")


def appointment(request, id):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id": ObjectId(id)})
    email = user["Email"]

    if not AdminDetails.objects.filter(email=email).exists():
        return redirect("/Home/")

    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    # Handle settings form submission
    if request.method == "POST":
        slot_duration = request.POST.get("slot-duration")
        advance_booking = request.POST.get("advance-booking")
        first_slot_time = request.POST.get("first-slot-time")
        slots_per_day = request.POST.get("slots-per-day")

        update_data = {
            "adminID": id,
            "Slot_Duration": int(slot_duration),
            "Advance_Booking": int(advance_booking),
            "First_Slot_Time": first_slot_time,
            "Slots_Per_Day": int(slots_per_day),
            "Time": datetime.now()
        }

        admin_settings.update_one(
            {"Form_Name": "Appointment_Settings"},
            {"$set": update_data},
            upsert=True
        )
        return redirect(f"/Admin/Custom/Appointments/{id}/")
    
    admin_data = admin_settings.find_one({"Form_Name": "Appointment_Settings"})
    slot_duration = int(admin_data["Slot_Duration"])
    slots_per_day = int(admin_data["Slots_Per_Day"])
    first_slot_time = admin_data["First_Slot_Time"]
    advance_booking = int(admin_data["Advance_Booking"])



    start_time = datetime.strptime(first_slot_time, "%H:%M")
    day_slots = [start_time.strftime("%I:%M %p")]
    
    for i in range(1, slots_per_day):
        next_time = start_time + timedelta(minutes= (i*slot_duration))
        day_slots.append(next_time.strftime("%I:%M %p"))  # 12-hour format
    
    user_appointments = []
    for i in appointments.find().sort("AppointmentDate", -1):
        i["aid"] = str(i["_id"])
        user_appointments.append(i)

    context = {
        "Image": image,
        "id": id,
        "admin_name": AdminDetails.objects.get(email=email).name,
        "appointment_settings": admin_settings.find_one({"Form_Name": "Appointment_Settings"}),
        "advance_booking" : advance_booking,
        "range" : range(7),
        "day_slots" : day_slots,
        "appointments" : user_appointments
    }
    return render(request, 'Admin/admin_appointment.html', context)



def mapViewer(request,id,aid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id": ObjectId(id)})
    email = user["Email"]

    try:
        image = dp.objects.get(email=email).profilepic
    except:
        image = None

    if not AdminDetails.objects.filter(email=email).exists():
        return redirect("/Home/")
    
    appointment = appointments.find_one({"_id" : ObjectId(aid)})
    address = ast.literal_eval(appointment["Address"])

    context = {
        "Address" : address,
        "Image": image,
        "id": id,
    }
    return render(request,"Admin/address_viewer.html",context) 


def cancelAppointment(request,id,aid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (id != request.session.get("user_id")):
        return redirect("/Home/")
    

    user = userdata.find_one({"_id": ObjectId(id)})
    email = user["Email"]

    if not AdminDetails.objects.filter(email=email).exists():
        return redirect("/Home/")
    
    appointments.update_one({"_id" : ObjectId(aid)},
                            {"$set" : {
                                "Status" : "Cancelled"
                            }})

    return redirect(f"/Admin/Custom/Appointments/{id}/")