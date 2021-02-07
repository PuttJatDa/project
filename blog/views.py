from django.shortcuts import render , HttpResponse,redirect
from .models import Post
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.
def blogHome(request):
    if not str(request.user)=='AnonymousUser':
        user=User.objects.get(username=request.user.username)

        allPosts=Post.objects.filter(author=user)
        context={'allPosts':allPosts}
        return render(request,'blog/blogHome.html',context)
    else:
        messages.error(request,"Please login to view this")
        return redirect('home')

def blogPost(request,slug):
    #return HttpResponse(f'This is blogPost: {slug}')
    post=Post.objects.filter(slug=slug).first()
    context={'post':post}
    return render(request,'blog/blogPost.html',context)
def createNewArticle(request):

    if not str(request.user)=='AnonymousUser':
        if request.method == "POST":
            title=request.POST['title']
            content=request.POST['content']
            img=request.FILES['img']
            author=User.objects.get(username=request.user.username)
            random_slug1=random.randint(0,9999)
            random_slug2=random.randint(0,9999)
            title_slug=''
            j=0
            for i in str(title):
            	if i==' ':
            		if j==0:
            			title_slug+='-'
            			j=1
            		else:
            			title_slug+=''

            	else:
            		title_slug+=i
            		j=0
            slug=str(random_slug1)+'-'+title_slug+str(random_slug2)
            public=request.POST['dropdown']
            timeStamp=datetime.now()
            newArtical=Post(title=title,img=img,content=content,author=author,slug=slug,public=public,timeStamp=timeStamp)
            newArtical.save()
            return redirect('/blog')
        else:
            return render(request,'blog/createNewArticle.html')
    else:
        messages.error(request,"Please login to Create file")
        return redirect('home')

