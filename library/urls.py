"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import home, contactus, register_view, update_profile

urlpatterns = [
	url(r'^$', home, name="index"),
    url(r'^register/$', register_view, name='register'),
    url(r'^update/$', update_profile, name='update'),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^u/', include('users.urls', namespace="users")),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^books/', include('books.urls', namespace='books')) ,
    url(r'^staff/', include('staff.urls', namespace='staff')),
    url(r'^contact/', contactus, name='contact'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),

]

# urlpatterns = [
#     url(r'^$', homepage, name='index'),
#     url(r'^register/', register_view, name='register'),
#     url(r'^login/', login_view, name='login'),
#     url(r'^logout/', logout_view, name='logout'),
#     url(r'^u/', include('users.urls', namespace="users")),
#     url(r'^admin/', admin.site.urls),
#     url(r'^books/', include('books.urls', namespace='books')) ,
#     url(r'^staff/', include('staff.urls', namespace='staff')),
#     url(r'^contact/', contactus, name='contact'),
#     url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
