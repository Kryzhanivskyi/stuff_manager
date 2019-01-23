from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from apps.account.models import User, ContactUs, RequestDayOffs
from apps.account.forms import ProfileForm, ContactUsForm, RequestDayOffForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.account.tasks import send_email_async
from django.core.cache import cache
from django.views.decorators.cache import cache_page



def index(request):
    # task_number_one.delay()
    # task_number_one()
    key = 'user_cache'
    if key in cache:  # check if users exist in cache
        users = cache.get(key)  # get users from cache
        print('11'*100)
    else:
        users = list(User.objects.all()[:100])  # get users from db
        cache.set(key, users, 15)  # set cache with key='user_cache', write 100 users for 15 seconds
        print('222'*100)
    # cache.delete(key)  # to delete cache by key


    # 1
    send_email_async.delay(
        'Subject here',
        'Here is the message.',
        user=request.user.id,
        from_email='bobertestdjango@gmail.com',
        recipient_list=['kryzhkot@gmail.com'],
    )

    # 2
    # send_email_async.apply_async(
    #     args=('Subject here', 'Here is the message.'),
    #     kwargs={'from_email': 'from@example.com',
    #             'recipient_list': ['to@example.com']},
    #     countdown=60 * 45,  # 45 min
        # countdown=10,
     # )
    # from datetime import datetime, timedelta
    # tomorrow = datetime.now() + timedelta(days=1)
    #
    # send_email_async.apply_async(
    #     args=('Subject here', 'Here is the message.'),
    #     kwargs={'from_email': 'from@example.com',
    #             'recipient_list': ['to@example.com']},
    #     eta=tomorrow,
    #  )
    return HttpResponse("Index")


@cache_page(10)
def cache_test(request):
    from time import sleep
    sleep(10)
    return HttpResponse('Cache Test')


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


@cache_page(60 * 5)
def faq(request):
    return render(request, "faq/faq.html")


@cache_page(60 * 5)
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

@login_required
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