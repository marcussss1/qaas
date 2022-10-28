"""DanilaAsked URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('new_ask/', views.new_ask),
    path('question/<int:i>', views.question),
    path('answers/<int:i>', views.answers),
    path('settings/', views.settings),
    path('tags/<str:tag_name>', views.tag),
    path('login/', views.login),
    path('login/registration/', views.registration),
    path('exit/', authViews.LogoutView.as_view(next_page=''), name='exit'),
]

