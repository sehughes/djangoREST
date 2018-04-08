from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Cm

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class CmCreateForm(ModelForm):
    class Meta:
        model = Cm
        fields = ("code", "ip_space", "netmask", "gateway_ip","description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].label = "Contract Manufacturer"
        self.fields["ip_space"].label = "IP Space"
        self.fields["netmask"].label = "Netmask"
        self.fields["gateway_ip"].label = "Gateway IP"
        self.fields["description"].label = "Description"

