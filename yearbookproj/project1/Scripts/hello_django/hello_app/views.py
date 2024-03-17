from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='signin')
def print_hello(request):
    return render (request,'index.html')
def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if(password==password2):
            if User.objects.filter(email=email).exists():
                messages.info(request,'This email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                #Create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
            
        else:
            messages.info(request,'Password does not match!')
            return redirect('signup')
    else:
        return(render(request,'signup.html'))

def signin(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('hello')
        else:
            messages.info(request,"Invalid credentials")
            return redirect('signin/')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')    
def logout(request):
    auth.logout(request)
    return redirect('signin')
@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        if request.FILES.get('image')==None:
            image= user_profile.profileimg
            bio=request.POST['bio']
            almamaters=request.POST['almamaters']
            workingat=request.POST['workingat']
            interests=request.POST['interests']
            user_profileimg=image
            user_profile.bio=bio
            user_profile.almamaters=almamaters
            user_profile.workingat=workingat
            user_profile.interests=interests
            user_profile.save()
        if request.FILES.get('image')!=None:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            almamaters=request.POST['almamaters']
            workingat=request.POST['workingat']
            interests=request.POST['interests']
            user_profileimg=image
            user_profile.bio=bio
            user_profile.almamaters=almamaters
            user_profile.workingat=workingat
            user_profile.interests=interests
            user_profile.save()
        return redirect('/settings')

    return render(request,'setting.html',{'user_profile':user_profile})
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    context={
        'user_object': user_object,
        'user_profile': user_profile,
    }
    
    return render(request,'profile.html',context)
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method=='POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list = []
        for users in username_object:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        #username_profile_list= list(chain(*username_profile_list))
    return render(request, 'search.html',{'user_profile': user_profile})

def yearbook(request):
    return render(request,'yearbook.html') 