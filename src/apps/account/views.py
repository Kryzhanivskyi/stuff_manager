from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from apps.account.models import User, ContactUs, RequestDayOffs
from apps.account.forms import ProfileForm, ContactUsForm, RequestDayOffForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required



def index(request):
    return HttpResponse("Index")



def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return redirect('redirect to a new page')


@login_required
def profile(request):
    user = request.user
    # user = get_object_or_404(User, id=user_id)

    form = ProfileForm(instance=user)
    if request.method == "GET":
        form = ProfileForm(instance=user)
    elif request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse("account:index"))
    context = {"form": form}


    with open('./info.txt', 'a') as the_file:
        ipaddress = request.META.get('REMOTE_ADDR')
        device = request.META.get("HTTP_USER_AGENT")
        the_file.write(f'IP_address:{ipaddress}\ndevice:{device}\n\n')




    return render(request, "account/profile.html", context=context)
    #return HttpResponse(f"{user.age}")


def contact_us(request):
    form_us = ContactUsForm()
    if request.method == "GET":
        form_us = ContactUsForm()
    elif request.method == "POST":
        form_us = ContactUsForm(request.POST)
        if form_us.is_valid():
            form_us.save()
            user_form = ContactUs.objects.last()
            send_mail(user_form.title, user_form.text, "bobertestdjango@gmail.com", [user_form.email])
    context = {"form": form_us}
    return render(request, "account/contact-us.html", context=context)


def faq(request):
    return render(request, "faq/faq.html")


def tos(request):
    return render(request, "tos/tos.html")


# def request_day_offs(request, user_id):
#     form_request = RequestDayOffsForm()
#     if request.method == "GET":
#         form_request = RequestDayOffsForm()
#     elif request.method == "POST":
#         form_request = RequestDayOffsForm(request.POST)
#         if form_request.is_valid():
#             form_request.save()
#             id_ = RequestDayOffs.objects.last()
#             id_.user = user_id
#             id_.save()
#
#     context = {"form": form_request}
#     return render(request, "form-request/form-request.html", context=context)

def create_request(request):
    user = request.user
    base_form = RequestDayOffForm

    if request.method == "GET":
        form = base_form(user=user)
    elif request.method == "POST":
        form = base_form(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:index'))
    context = {'form': form}
    return render(request, 'account/create-request.html',
                  context=context)