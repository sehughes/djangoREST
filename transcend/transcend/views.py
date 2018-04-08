from django.views.generic import TemplateView

class sitesPage(TemplateView):
    template_name = 'sites.html'

class loggedInPage(TemplateView):
    template_name = 'loggedIn.html'

class loggedOutPage(TemplateView):
    template_name = 'loggedOut.html'

class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)