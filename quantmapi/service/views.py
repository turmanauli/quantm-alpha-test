from django.http import HttpResponse
from django.template import loader

# Create your views here.
def main_view(request):
    t = loader.get_template("index.html")
    c = {"foo": "bar"}
    return HttpResponse(t.render(c, request), content_type="text/html")