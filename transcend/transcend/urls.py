"""transcend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from . import views
from accounts import views as accounts_views

urlpatterns = [
    url(r"^$", views.HomePage.as_view(), name="home"),
    url(r"^loggedIn/$", views.loggedInPage.as_view(), name="loggedIn"),
    url(r"^loggedOut/$", views.loggedOutPage.as_view(), name="loggedOut"),
    url(r"^cm_list/$", accounts_views.CmListView.as_view(template_name="cm/cm_list.html"), name='cm_list'),
    url(r"^admin/", admin.site.urls),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
]
