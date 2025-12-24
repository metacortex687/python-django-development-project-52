from django.views.generic.base import TemplateView
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = "index.html"


def test_rollbar(request):
    a = None
    a.test_rollbar()
    return HttpResponse("test_error_in_rollbar")
