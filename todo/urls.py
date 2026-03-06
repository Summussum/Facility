"""
URL configuration for facility project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('schedule_type_select', views.schedule_type_select, name="schedule_type_select"),
    path('create_task/', views.create_task, name="create_task"),
    path('log_task/<int:task_id>', views.log_task, name="log_task"),
    path('bump_task/<int:task_id>', views.bump_task, name="bump_task"),
    path('pause_task/<int:task_id>', views.pause_task, name="pause_task")
]
