from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from apps.account.models import User

def index(request):
    return HttpResponse("Index")

def profile(request, user_id):
    #try:
    #    user = User.objects.get(id=user_id)
    #except User.DoesNotExist:
    #    raise Http404
    user = get_object_or_404(User, id=user_id)

    return HttpResponse(f"{user}")
