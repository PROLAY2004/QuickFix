from django.shortcuts import render,redirect
from django.conf import settings
from bson import ObjectId
from .models import dp
from main_app.models import AdminDetails
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib import messages

# Create your views here.
userdata = settings.MONGO_DB.userdata
services = settings.MONGO_DB.services
appointments = settings.MONGO_DB.appointments
blocked_slots = settings.MONGO_DB.blocked_slots
admin_settings = settings.MONGO_DB.admin_settings

# Create your views here.
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from .models import dp  # Assuming dp is your Django model for profile pictures

def dashboard(request, userid):
    user = userdata.find_one({"_id": ObjectId(userid)})
    
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}/")

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
                {"_id": ObjectId(userid)},
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

        return redirect(f"/Dashboard/{userid}/")

    if dp.objects.filter(email = user["Email"]).exists():
        temp = dp.objects.get(email = user["Email"]).profilepic
    else:
        temp = None
        
    flag = False
    try:
        location = user["Address"]
        for i in location:
            if (i["Default_Address"]):
                flag = True
    except:
        location = None

    context = {
        "id": userid,
        "user": user,
        "image" : temp,
        "address" : location,
        "Default_exist" : flag
    }
    return render(request, 'Accounts/Profile.html', context)



def location(request, userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    if request.method == 'POST':
        is_checked = request.POST.get('is_default') == 'on' # Get checkbox value - returns 'on' if checked, missing if unchecked
        if(is_checked):
            condition  = True
        else:
            condition = False

        Address = {
            "latitude" : request.POST.get("latitude"),
            "longitude" : request.POST.get("longitude"),
            "add_name" : request.POST.get("name"),
            "mob" : request.POST.get("phone"),
            "street" : request.POST.get("street"),
            "city" : request.POST.get("city"),
            "state" : request.POST.get("state"),
            "pin" : request.POST.get("zip_code"),
            "country" : request.POST.get("country"),
            "Default_Address" : condition
        }

        Address_exists = userdata.find_one({
            '_id': ObjectId(userid),
            'Address': {'$exists': True}
        })
        if not Address_exists:
            user = userdata.find_one({'_id': ObjectId(userid)})
            userdata.update_one({'_id': ObjectId(userid)},{"$set" : { "Address" : [Address] }})
            url = "/Dashboard/" + userid + "/"
            return redirect(url)

        else:
            user = userdata.find_one({'_id': ObjectId(userid)})
            address = user["Address"]
            address.append(Address)
            userdata.update_one(
                {'_id': ObjectId(userid)},
                {"$set" : { "Address" : address}}
            )
            url = "/Dashboard/" + userid + "/"
            return redirect(url)
    else:
        try:
            user = userdata.find_one({'_id': ObjectId(userid)})
            alladdress = user["Address"]
            checkbox = True
            for i in alladdress:
                if (i["Default_Address"]):
                    checkbox = False
        except:
            checkbox = True

        context = {
            "Heading" : "Add New Address",
            "Default_exist" : checkbox
        }
        return render(request,"Accounts/location.html",context)
    

def delAddr(request,index,userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    user = userdata.find_one({'_id': ObjectId(userid)})
    alladdress = user["Address"] #This is the Array
    address_to_remove = alladdress[index] 

    userdata.update_one(
        {"_id" : ObjectId(userid)},
        {"$pull": {"Address": address_to_remove}}
    )

    url = "/Dashboard/" + userid + "/"
    return redirect(url)
    

def editAddr(request,index,userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    user = userdata.find_one({'_id': ObjectId(userid)})
    alladdress = user["Address"] #This is the Array
    address_to_edit = alladdress[index]
    

    if request.method == "POST":
        is_checked = request.POST.get('is_default') == 'on' # Get checkbox value - returns 'on' if checked, missing if unchecked
        if(is_checked):
            condition  = True
        else:
            condition = False

        Address = {
            "latitude" : request.POST.get("latitude"),
            "longitude" : request.POST.get("longitude"),
            "add_name" : request.POST.get("name"),
            "mob" : request.POST.get("phone"),
            "street" : request.POST.get("street"),
            "city" : request.POST.get("city"),
            "state" : request.POST.get("state"),
            "pin" : request.POST.get("zip_code"),
            "country" : request.POST.get("country"),
            "Default_Address" : condition
        }            

        userdata.update_one(
            {"_id" : ObjectId(userid)},
            {"$set": {f"Address.{index}": Address}}
        )

        url = "/Dashboard/" + userid + "/"
        return redirect(url)

    if(address_to_edit["Default_Address"]):
        temp = "Checked"
    else:
        temp = None

    context = {
        "Heading" : "Edit Address",
        "Address" : address_to_edit,
        "default" : temp
    }
    return render(request,"Accounts/edit_location.html",context) 
    

def setDefault(request,index,userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    user = userdata.find_one({'_id': ObjectId(userid)})
    alladdress = user["Address"]

    userdata.update_one(
        {"_id" : ObjectId(userid)},
        {"$set": {f"Address.{index}.Default_Address": True}}
    )

    url = "/Dashboard/" + userid + "/"
    return redirect(url)
    

def orders(request,userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}/")

    context = {
        "id" : userid
    }
    return render(request,'Accounts/orders.html',context)


def slots(request, userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif userid != request.session.get("user_id"):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email=request.session.get("user_email")).exists():
        if not AdminDetails.objects.get(email=request.session.get("user_email")).is_superAdmin:
            return redirect(f"/Admin/Custom/{userid}")
        
    if request.method == "POST":
        service_type = request.POST.get("service-type")
        service_details = request.POST.get("service-details")
        appointment_date = request.POST.get("appointment-date")
        appointment_time = request.POST.get("appointment-time")
        name = request.POST.get("full-name")
        mobile = request.POST.get("phone")
        address = request.POST.get("address")
        notes = request.POST.get("notes")


        appointments.insert_one({
            "userID": userid,
            "Name": service_type,
            "Details": service_details,
            "AppointmentDate": appointment_date,
            "AppointmentTime": appointment_time,
            "userName": name,
            "Mobile": mobile,
            "Address": address,
            "Notes": notes,
            "BookingTime": datetime.now(),
            "Status": "Pending"
        })

        return redirect(f"/Dashboard/Appointment/{userid}/")
    

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
    for i in appointments.find({"userID": userid}).sort("AppointmentDate", -1):
        i["aid"] = str(i["_id"])
        user_appointments.append(i)

    context = {
        "id": userid,
        "services": services.find(),
        "user": userdata.find_one({"_id": ObjectId(userid)}),
        "appointments": user_appointments,
        "admin_settings" : admin_data,
        "range" : range(7),
        "day_slots" : day_slots,
        "advance_booking" : advance_booking
    }
    return render(request, 'Accounts/appoinment.html', context)
    


def delAppointment(request,userid,appointmentid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    if not (appointments.find_one({"_id" : ObjectId(appointmentid), "userID" : userid})):
        return redirect(f"/Dashboard/Appointment/{userid}/")
    else:
        appointments.delete_one({"_id" : ObjectId(appointmentid), "userID" : userid})
        return redirect(f"/Dashboard/Appointment/{userid}/")


def setting(request,userid):
    if not request.session.get("user_id"):
        request.session["redirect_path"] = request.path
        return redirect("/Auth/Login/")
    elif (userid != request.session.get("user_id")):
        return redirect("/Home/")
    elif AdminDetails.objects.filter(email = request.session.get("user_email")).exists():
        if (AdminDetails.objects.get(email = request.session.get("user_email")).is_superAdmin == False):
            return redirect(f"/Admin/Custom/{userid}")
    
    context = {
        "id" : userid
    }
    return render(request,'Accounts/settings.html',context)