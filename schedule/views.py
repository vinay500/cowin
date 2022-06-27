from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from CPD_app.models import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request,'home.html')


def schedule(request):
    if "aadhaar" in request.session:
        if request.method=='POST':
            aadhaar = request.session['aadhaar']
            user_obj=Users.objects.get(aadhaar_number=aadhaar)
            aadhaar_number=user_obj.aadhaar_number
            print(aadhaar_number)
            print("user:",user_obj)
            state=request.POST['state']
            district=request.POST['district']
            vaccine=request.POST['vaccine']
            slot=request.POST['slot']
            print(state,district,vaccine,slot)
            slot = SlotBook(state=state,district=district,vaccine=vaccine,slot=slot,aadhaar=user_obj)
            slot.save();
            messages.success(request,'Slot Booked')
            return redirect('/scheduleslots_booked')
        else:
            return render(request, 'schedule.html')
    else:
        # messages.error(request,"Login again")
        return render(request,'login.html')

def slots_booked(request):
    if "aadhaar" in request.session:
        aadhaar = request.session['aadhaar']
        print("aadhaar in session:",aadhaar)
        # user = SlotBook.objects.all().prefetch_related('aadhaar')
        slots = SlotBook.objects.filter(aadhaar=aadhaar)
        print("slot booked users",slots)
        # print(slots[0].name,slots.aadhaar,slots.photo_id_proof,slots.year_of_birth,)
        # print(slots[0].aadhaar.name)
        # print(slots[0].aadhaar.year_of_birth)
        # print(slots[0].vaccine)
        return render(request,'slots.html',{"slots":slots})

    messages.error(request,"session out")
    return render(request,'slots.html')

def logout(request):
    if ("aadhaar" in request.session) and ("mobile" in request.session) and ("otp" in request.session):
        request.session.flush()
        # request.session['aadhaar']
        # request.session['mobile']
        # request.session['otp']
        print("sessions flushed")
        return redirect('/')
    else:
        print("sessions unflushed or doesn't exist")
        return redirect('/')
