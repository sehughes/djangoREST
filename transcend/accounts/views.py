from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import Cm
from . import forms

# Sign up form for new test operators and other partner operatives
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

#  CRUD operations for CMs
class CmListView(ListView):
    model = Cm

    def get_queryset(self):
        return Cm.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class CmCreateView(CreateView):
    model = Cm
    fields = ['code', 'ip_space', 'netmask', 'gateway_ip', 'description']

class CmUpdateView(UpdateView):
    model = Cm
    fields = ['code', 'ip_space', 'netmask', 'gateway_ip', 'description']
    template_name_suffix = '_update_form'

class CmDeleteView(DeleteView):
    model = Cm
    success_url = reverse_lazy('cm-list')