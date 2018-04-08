from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r"cm_list/$", views.CmListView.as_view(template_name="cm/cm_list.html"), name='cm_list'),
    url(r"cm_create/$", views.CmCreateView.as_view(template_name="cm/cm_create.html"), name='cm_create'),
    url(r"cm_update/$", views.CmUpdateView.as_view(template_name="cm/cm_update.html"), name='cm_update'),
    url(r"cm_delete/$", views.CmDeleteView.as_view(template_name="cm/cm_delete.html"), name='cm_delete'),
]
