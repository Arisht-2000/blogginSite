from django.shortcuts import render
from blogapp.models import BlogArticle
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User,Group
#from django.views.decorators.csrf import csrf_exempt
#from django.http import HttpResponse
#from django.http import JsonResponse
#from django.conf import settings

# Create your views here.
def index(request):
    blogs = BlogArticle.objects.all()
    if request.method == 'POST':
        usname = request.POST['username']
        pwd = request.POST['password']
        try:
            u = User.objects.get(username=usname)
        except:
            email = request.POST['email']
            cnfPass = request.POST['cnfrm_password']
            if cnfPass == pwd:
                user = User.objects.create_user(usname, email, pwd)
                my_group = Group.objects.get(name='USERS_OF_BLOGAPP')
                my_group.user_set.add(user)
            else:
                return render(request, "main.html", {"testvar":"Test String 2!",'blogs':blogs, 'user':None})
        user = authenticate(username=usname, password=pwd)
        if user is not None:
            login(request, user)
            return render(request, "main.html", {"testvar":"Test String 2!",'blogs':blogs, 'user':user})
    return render(request, "main.html", {"testvar":"Test String 2!",'blogs':blogs, 'user':None})

@permission_required('blogapp.add_blog', raise_exception=True)
def createblog(request):
    newBlog = BlogArticle()
    newBlog.title = request.POST['title']
    newBlog.author = request.user
    newBlog.blog_content = request.POST['blog_content']
    newBlog.save()
    user = request.user
    blogs = BlogArticle.objects.all()
    return render(request, "main.html", {"testvar":"Test String 2!",'blogs':blogs, 'user':user})

def logout_view(request):
    blogs = BlogArticle.objects.all()
    if request.method == 'POST':
        logout(request)
        return render(request, "main.html", {"testvar":"Test String 2!",'blogs':blogs, 'user':None})