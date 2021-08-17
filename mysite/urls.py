"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from accounts import views as accounts_views
from ideabook import views as ideabook_views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('',ideabook_views.feedview,name='feed'),
    path('like-idea/<int:pk>/',ideabook_views.like_idea,name='like_idea'),
    path('<int:pk>/',ideabook_views.ideaview,name='idea'),
    path('my_account/',ideabook_views.myaccountview,name='my_account'),
    path('delete/<int:pk>/', ideabook_views.delete_idea, name='delete_idea'),
    path('edit_idea/<int:pk>/', ideabook_views.edit_idea, name='edit_idea'),
    path('signup/',accounts_views.signup,name='signup'),
    path('setup_profile/',accounts_views.setup_profile,name='setup_profile'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('admin/', admin.site.urls),
]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
