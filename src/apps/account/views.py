from django.http import HttpResponse
from .models import User


def profile(request, id):
    return HttpResponse(User.objects.filter(id=id))
