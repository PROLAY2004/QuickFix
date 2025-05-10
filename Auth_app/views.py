from django.shortcuts import render,redirect,HttpResponse
import random
from bson import ObjectId
from datetime import datetime
from django.conf import settings
from pymongo import DESCENDING
import requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Create your views here.
userdata = settings.MONGO_DB.userdata
otplist = settings.MONGO_DB.otps


# Generate a unique otp for all time
def generate_OTP():
    temp = random.randint(100000,999999)
    if (otplist.find_one({"otp":temp})):
        return generate_OTP()
    else:
        return temp

# Handel login operations
def signin(request):
    if(request.session.get("user_id")):
        return redirect("Home")
    else:
        email = request.POST.get("mail")
        if(email):
            temp = generate_OTP()
            otplist.insert_one({
                "Email": email,
                "OTP" : temp,
                "Time" : datetime.now()
                })
            print(temp)
            id = otplist.find_one({"OTP" : temp})["_id"]
            url = "/Auth/Login/" + str(id)
            return redirect(url)
        else:
            return render(request,'Authentication/login.html')
        

def verify(request,id):
    if(otplist.find_one({"_id" : ObjectId(id)})):
        otp = request.POST.get("otp")
        mail = otplist.find_one({"_id" : ObjectId(id)})["Email"]
        if(otp):
            if(len(otp) == 6):
                if(otplist.find_one({"OTP" : int(otp), "Email" : mail})):
                    if (otplist.find_one({"Email" : mail},sort=[('_id', DESCENDING)])["OTP"] == int(otp) ):
                        if(userdata.find_one({"Email" : mail})):
                            user = userdata.find_one({"Email" : mail})
                            request.session["user_id"] = str(user["_id"])
                            request.session["user_email"] = user["Email"]
                            url = request.session.get("redirect_path")
                            return redirect(url)
                        else:
                            userdata.insert_one({"Email" : mail, "Time" : datetime.now()})
                            user = userdata.find_one({"Email" : mail})
                            request.session["user_id"] = str(user["_id"])
                            request.session["user_email"] = user["Email"]
                            url = request.session.get("redirect_path")
                            return redirect(url)
                    else:
                        context = {
                            "user_email" : mail,
                            "message" : "OTP Expired."
                        }
                        return render(request,'Authentication/verify.html',context) 
                else:
                    context = {
                        "user_email" : mail,
                        "message" : "Invalid OTP."
                    }
                    return render(request,'Authentication/verify.html',context)
            else:
                context = {
                    "user_email" : mail,
                    "message" : "OTP Should be 6 Digits."
                }
                return render(request,'Authentication/verify.html/',context)
            
        context = {
            "user_email" : mail
        }
        return render(request,"Authentication/verify.html",context)
    else:
        return redirect("/Auth/Login/")


#Google Authentication
def google(request):
    if request.session.get("user_id"):
        return redirect("Home")
    
    # Handle the Google callback
    code = request.GET.get('code')
    if not code:
        print("No_Code")
        return redirect("Login")
    print("Code Recived...")
    # Exchange the authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        tokens = response.json()
        
        # Debugging: Print the token response
        print("Token response:", json.dumps(tokens, indent=2))
        
        if 'id_token' not in tokens:
            # If no id_token, try to get user info using access_token
            if 'access_token' in tokens:
                userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
                headers = {'Authorization': f'Bearer {tokens["access_token"]}'}
                userinfo_response = requests.get(userinfo_url, headers=headers)
                userinfo_response.raise_for_status()
                user_info = userinfo_response.json()
                email = user_info['email']

            else:
                return redirect("/Auth/Login/")
        else:
            # Verify the ID token if present
            idinfo = id_token.verify_oauth2_token(
                tokens['id_token'],
                google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID
            )
            email = idinfo['email']
        
        # Check if user exists in MongoDB
        if userdata.find_one({"Email": email}):
            user = userdata.find_one({"Email": email})
        else:
            # Create new user
            userdata.insert_one({
                "Email": email,
                "Time": datetime.now()
            })
            user = userdata.find_one({"Email": email})
        
        # Set session
        request.session["user_id"] = str(user["_id"])
        request.session["user_email"] = user["Email"]
        
        url = request.session.get("redirect_path")
        return redirect(url)
    
    except Exception as e:
        print(f"Google auth error: {str(e)}")
        return redirect("/Auth/Login/")


#Handel Logout Requests
def signout(request):
    request.session.flush()
    return redirect("/Home/")