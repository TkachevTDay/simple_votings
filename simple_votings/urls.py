"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('time/', views.time_page, name='time'),
    path('votings/', views.votings, name='votings'),
    path('profile/', views.profile, name='profile'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'menu': views.get_menu_context(),
                'pagename': 'Авторизация'
            }
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vote/<int:vote_id>/', views.vote_page, name='vote'),
    path('vote/add/', views.add_voting, name='vote_add'),
    path('vote/<int:vote_id>/', views.vote_page, name='vote'),
    path('registration/', views.register, name='registration')
]
