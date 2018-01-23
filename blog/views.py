from email.iterators import body_line_iterator

from django.contrib.messages.context_processors import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import article, category, author, comment
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import createFrom,registerUser, createAuthor, commentForm
from django.contrib import messages

# Create your views here.
def index(request):
    post=article.objects.all()
    search= request.GET.get('p')
    if search:
        post=post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    paginator = Paginator(post, 24)  # Show 24 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context={"post":total_article}
    return render(request,"index.html", context)

def getauthor(request,name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    post = article.objects.filter(article_author=auth.id)
    context={
        "post":post,
        "auth":auth
    }
    return render(request,"profile.html",context)

def getsingle(request,id):
    post=get_object_or_404(article,pk=id)
    first=article.objects.first()
    last=article.objects.last()
    getcomment=comment.objects.filter(post=id)
    related=article.objects.filter(category=post.category).exclude(id=id)[:4]
    form=commentForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
    context={
        "post":post,
        "first":first,
        "last":last,
        "related":related,
        "form":form,
        "comment":getcomment
    }
    return render(request,"single.html", context)

def gettopic(request,name):
    cat=get_object_or_404(category,name=name)
    post=article.objects.filter(category=cat.id)
    return render(request,"category.html",{"post":post,"cat":cat})

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password does not match!')
    return render(request,"login.html")

def getlogout(request):
    logout(request)
    return redirect('index')

def getCreate(request):
    if request.user.is_authenticated:
        u=get_object_or_404(author,name=request.user.id)
        form = createFrom(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.success(request, 'Article is published successfully!')
            return redirect('profile')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('login')

def getUpdate(request,id):
    if request.user.is_authenticated:
        u=get_object_or_404(author,name=request.user.id)
        post=get_object_or_404(article,id=id)
        form = createFrom(request.POST or None, request.FILES or None,instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.success(request,'Article is updated successfully!')
            return redirect('profile')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('login')

def getDelete(request,id):
    if request.user.is_authenticated:
        post=get_object_or_404(article,id=id)
        post.delete()
        messages.warning(request, 'Article is deleted successfully!')
        return redirect('profile')
    else:
        return redirect('login')

def getProfile(request):
    if request.user.is_authenticated:
        user= get_object_or_404(User,id=request.user.id)
        author_profile= author.objects.filter(name=user.id)
        if author_profile:
            userauthor = get_object_or_404(author,name=request.user.id)
            post= article.objects.filter(article_author=userauthor.id)
            return render(request,'login_profile.html',{"post":post,"user":userauthor})
        else:
            form=createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.name=user
                instance.save()
                return redirect('profile')
            return render(request,'createauthor.html',{"form":form})

    else:
        return render(request, 'login.html')

def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,'Registration Successfully!')
        return redirect('login')
    return render(request,'register.html',{"form":form})