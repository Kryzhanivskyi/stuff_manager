from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta, datetime

from apps import model_choices as mch

@shared_task
def task_number_one():
    print('Hello from number One')


@shared_task
def increment_dayoffs():
    from apps.account.models import User

    for user in User.objects.all().iterator():
        # TODO
        try:
            user.sickness_days += 2
            user.vacation_days += 2
            user.save()
            # send_email_async.delay(user)
        except Exception:
            pass


@shared_task
def send_email_async(*args, **kwargs):
    from apps.account.models import User

    user_id = kwargs.pop('user')
    user = User.objects.get(id=user_id)

    send_mail(*args, **kwargs)
    #     subject='Subject here',
    #     message='Here is the message.',
    #     from_email='from@example.com',
    #     recipient_list=['to@example.com'],
    #     fail_silently=False,
    # )


@shared_task
def request_date_check():
    from apps.account.models import RequestDayOffs
    for request in RequestDayOffs.objects.filter(status=mch.STATUS_PENDING).iterator():
        if (request.created + timedelta(days=30)) < datetime.now():
            request.status = mch.STATUS_PASSED
            request.save()
