from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForms, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section':'dashboard'})





def user_login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],
                                            password=cd['password'], )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticate')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForms()
    return render(request,'account/login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile Updated Successfully')
        else:
            messages.error(request,'Failed Update')     

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = { 'user_form':user_form, 'profile_form':profile_form}
    return render(request,'account/edit.html',context)