from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
import random
import http.client
from django.conf import settings
# from twilio.rest import Client


# Create your views here.
def home(request):

    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        photo_id_proof = request.POST['photo_id_proof']
        aadhaar_number_recieved = request.POST['aadhaar_number']
        name = request.POST['name']
        year_of_birth = request.POST['year_of_birth']
        gender = request.POST['gender']
        print(photo_id_proof,aadhaar_number_recieved,name,year_of_birth,gender)
        if Users.objects.filter(aadhaar_number = aadhaar_number_recieved).exists():
            # print(aadhaar_number_recieved)
           messages.error(request,'Aadhaar Number already Registered')
           return render(request,'register.html')
        else:
            user = Users(photo_id_proof=photo_id_proof, aadhaar_number=aadhaar_number_recieved, name=name,
                         year_of_birth=year_of_birth, gender=gender)
            user.save()
            print("user  logged in")
            return redirect('/login')
    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        aadhaar_number = request.POST['login_aadhaar_number']
        name = request.POST['name']
        year_of_birth = request.POST['year_of_birth']
        print(aadhaar_number,name,year_of_birth)
        # user = Users.objects.filter(aadhaar_number = aadhaar_number)
        # print(user)
        if Users.objects.filter(aadhaar_number = aadhaar_number).exists():
          print("user  exist")
          request.session['aadhaar']=aadhaar_number
          if 'aadhaar' in request.session:
              print("in session")
          return redirect('/schedulebook')
        else:
            print("user doesnot exist")
            messages.error(request,"""User Doesn't exists Register and Login""")
            return render(request,'register.html')
    return render(request, 'login.html')


def send_otp(mobile,otp):
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # headers = {
    #     'authkey': "",
    #     'content-type': "application/JSON"
    # }
    # authkey = settings.authkey
    # url="http://control.msg91.com/api/sendotp.php?otp"+otp+"&sender=nosenderid&message="+'Your otp is'+otp+'&mobile='+mobile+'&authkey='+authkey+'&country=91'
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"
    # headers = {'content-type': "application/json"}
    # conn.request("GET", "/api/v5/otp?template_id=&mobile=&authkey=", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    # print("otp sent",data.decode("utf-8"))

#     using twilio
    account_sid='AC08d990f2a7eea86ea4ac4d861230ab98'
    auth_token='4e68821d52db6c0a4b434d6ee2d28208'
    client=Client(account_sid,auth_token)

    message = client.messages.create(
        body = 'Your OTP is '+ otp,
        from_= '+14159850526',
        to = '+918555975391'
    )
    print(message.sid)

def otp(request):
    if request.method == 'POST':
        mobile=request.POST['mobile_number']
        print(mobile)
        # session_mobile=request.session['mobile']
        otp = str(random.randint(1000,9999))
        otp_obj=Otp(mobile=mobile,otp=otp)
        send_otp(mobile,otp)
        request.session['mobile'] = mobile
        request.session['otp'] = otp
        otp_obj.save()
        print(mobile,otp)
        return render(request,'otp_verify.html')
    # messages.error(request,"""Method='GET'""")
    return render(request,'otp.html')

def otp_verify(request):
    if request.method == 'POST':
        mobile=request.session['mobile']
        msg_otp=request.session['otp']
        verify_otp=request.POST['otp']
        print(mobile,msg_otp,verify_otp)
        if mobile and msg_otp:
            print("session alive")
            if msg_otp == verify_otp:
                return render(request, 'login.html')
            else:
                messages.error(request, 'Wrong OTP Entered')
                return render(request, 'otp_verify.html')
        else:
            messages.error(request, 'Session Timed-out,Try Again')
            return render(request, 'otp_verify.html')
    return render(request,'otp_verify.html')


def logout(request):
    try:
        if ("aadhaar" in request.session) or ("mobile" in request.session) or ("otp" in request.session):
            request.session.flush()
            # request.session['aadhaar']
            # request.session['mobile']
            # request.session['otp']
            print("sessions flushed")
            return redirect('/')
        else:
            print("sessions unflushed or doesn't exist")
            return redirect('/')
    except Exception as e:
        print(e)





