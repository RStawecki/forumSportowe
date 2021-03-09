"""forumSportowe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from forum import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #accounts
    path('auth/', include('accounts.urls')),
    path('verification/', include('verify_email.urls')),
    #forum
    path('', views.home, name='home'),
    path('latest', views.latest, name='latest'),
    path('create', views.create, name='create'),
    path('show_detail' , views.show_detail, name='show_detail'),
    path('show_detail/<int:questionId>', views.myDetail, name='myDetail'),
    path('show_detail/<int:questionId>/delete', views.delete, name='delete'),
    path('latest/<int:questionId>/detail', views.detail, name='detail'),
    path('sport/<str:sportKey>', views.displaySport, name='displaySport'),
    path('search/', views.search, name='search'),
    path('create_answer/<int:questionId>', views.createAnswer, name="create_answer"),
    path('edit_answer/<int:answerId>', views.edit_answer, name='edit_answer'),
    path('latest/<int:questionId>', views.like, name='like'),

    
]
#how to upload images
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
