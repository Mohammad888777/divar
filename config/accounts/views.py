from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from .forms import SignUpForm
from django.contrib.auth import login,authenticate,logout


def register(request):

    if request.method=="POST":
        phone=request.POST.get("phone_number")
        user=User.objects.filter(
            phone_number=phone
        ).exists()
        if not user:
            new_user=User.objects.create_user(
                phone_number=phone
            )
            login(request,new_user)
            return redirect("index")
        


    contex={
        'form':SignUpForm()
    }
    return render(request,"accounts/register.html",contex)
