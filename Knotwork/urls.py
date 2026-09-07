"""
URL configuration for Knotwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from Knot import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore', views.explore, name='explore'),
    path('skill-exchange', views.skill_exchange, name='skill_exchange'),
    path('how-it-works', views.how_it_works, name='how_it_works'),
    path('get-started', views.get_started, name='get_started'),
    path('mentors', views.mentors, name='mentors'),
    path('communities', views.communities, name='communities'),
    path('pricing', views.pricing, name='pricing'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('help', views.help, name='help'),



    
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login, name='login'),
    




    # path('admin/', admin.site.urls),
]
