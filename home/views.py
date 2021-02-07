from django.shortcuts import render , HttpResponse,redirect
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random



# Create your views here.
def home(request):
    global str_num,num
    opr=["+","*","-"]
    random_num1=random.randint(1, 9)
    random_opr=random.choice(opr)
    random_num2=random.randint(1, 9)
    str_num=str(random_num1)+str(random_opr)+str(random_num2)
    if(random_opr=="+"):
        num=random_num1+random_num2
    elif(random_opr=="-"):
    	num=random_num1-random_num2
    elif(random_opr=="*"):
	    num=random_num1*random_num2
    if not str(request.user)=='AnonymousUser':
        user=User.objects.get(username=request.user.username)
        allPostsUser=Post.objects.filter(author=user)
        allPostsOther=Post.objects.filter(public=True)
        allPosts=allPostsUser.union(allPostsOther)
    else:
        allPosts=Post.objects.filter(public=True)
    context={"allPosts":allPosts,'img':str_num}
    return render(request,'home/home.html',context)
def about(request):
    
    context={'img':str_num}
    return render(request,'home/about.html',context)

def search(request):
    query=request.GET['query']
    allPostsTitle=Post.objects.filter(title__icontains=query, public=True)
    allPostsAuthor=Post.objects.filter(author__icontains=query, public=True)
    allPosts=allPostsTitle.union(allPostsAuthor)
    context={"allPosts":allPosts,'query':query}
    return render(request,'home/search.html',context)
def handleSignup(request):
    if request.method == 'POST':
        if request.method == 'POST':

            username=request.POST['username']
            email=request.POST['email']
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            cap=request.POST['captha']
            usercheck=User.objects.filter(username=username)
            if not len(usercheck) == 0:
                messages.error(request,'This username is already taken! Please try different one')
                return redirect('home')
            if not username.isalnum():
                messages.error(request,'Username must be Alphanumeric')
                return redirect('home')
            if len(username) > 15:
                messages.error(request,'Username must be under than 15 characters')
                return redirect('home')
            if not len(pass1) > 7:
                messages.error(request,'Password must have 8 characters')
                return redirect('home')
            digit=False
            alpha=False
            for i in pass1:
                if i.isdigit():
                    digit=True
                if i.isalpha():
                    alpha=True
            if not digit and alpha:
                messages.error(request,'Password must be Alphanumeric')
                return redirect('home')

            if pass1 != pass2:
                messages.error(request,"Password Doesn't Match")
                return redirect('home')
            
            if not str(cap)==str(num) :
                messages.error(request,'Your Captha is Wrong! Please Try again')
                return redirect('home') 

            myuser= User.objects.create_user(username,email,pass1)
            myuser.save()
            messages.success(request,'Your account has been successfully Created')
            user=authenticate(username=username,password=pass1)
            login(request,user)
            return redirect('/blog')
            

    
    else:
        return HttpResponse("Error 404 - not found")
def handleLogin(request):
    if request.method == 'POST':
        loginUsername=request.POST['loginUsername']
        
        loginPassword=request.POST['loginPassword']
        user=authenticate(username=loginUsername,password=loginPassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Login')
            return redirect('/blog')
        else:
            messages.error(request,"Invalid Login! Please Try again")
            return redirect('home')


    else:
        return HttpResponse("Error 404 - not found")
def handleLogout(request):

    logout(request)
    messages.success(request,"Sucessfully Logout")
    return redirect('home')
