"""simpleBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index' ),
    path('author/<name>',views.getauthor,name='author' ),
    path('article/<int:id>',views.getsingle,name='article' ),
    path('topic/<name>',views.gettopic,name='topic' ),
    path('login/',views.userLogin,name='login' ),
    path('logout/',views.getlogout,name='logout' ),
    path('create/',views.getCreate,name='create' ),
    path('profile/',views.getProfile,name='profile' ),
    path('update/<int:id>',views.getUpdate,name='update' ),
    path('delete/<int:id>',views.getDelete,name='delete' ),
    path('register/',views.getRegister,name='register' ),
]
