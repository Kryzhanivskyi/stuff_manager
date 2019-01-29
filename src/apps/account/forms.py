#from django.forms import ModelForm
from django import forms
from django.db.models import Q
from datetime import timedelta, datetime
from apps import model_choices as mch
from apps.account.models import User, ContactUs, RequestDayOffs
from apps.account.tasks import send_email_async


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'age', 'email',
            'first_name', 'last_name',
            'city'
        ]

    def save(self, commit=True):
        super().save(*args, **kwargs)


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = [
            'email',
            'title', 'text',
        ]


class RequestDayOffForm(forms.ModelForm):

    class Meta:
        model = RequestDayOffs
        fields = [
            'type', 'from_date', 'to_date', 'status_changed',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            #TODO спросить Диму, какого хуя дата должна юыть перед ифом а не после
            data = cleaned_data['to_date'] - cleaned_data['from_date']
            if cleaned_data['from_date'] > cleaned_data['to_date']:
                self.add_error('to_date', 'from_date cannot be greater then to_date')
            if cleaned_data["type"] == mch.REQUEST_DAYOFF and data.days > 1:
                self.add_error('to_date', 'dayoff should be not more then 1 day')
            date_from = cleaned_data['from_date']
            days_counter = 0
            for day in range(data.days):
                if date_from.isoweekday() == 6 or date_from.isoweekday() == 7:
                    date_from = date_from + timedelta(days=1)
                    continue
                else:
                    days_counter += 1
                    date_from = date_from + timedelta(days=1)
            if days_counter >= 20:
                self.add_error('to_date', "vacation shouldn't be less then 20 working days")
            if days_counter > self.user.vacations_days:
                self.add_error('type', "you have not enough days to get this vacation")
            return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class RequestDayOffAdminForm(forms.ModelForm):

    class Meta:
        model = RequestDayOffs
        fields = [
            'status', 'created', 'status_changed', 'from_date', 'to_date', 'reason', 'type',
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['type'] == mch.STATUS_REJECTED and not cleaned_data['reason']:
                self.add_error('reason', "reason field is required")
            return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = super().clean()
        data = cleaned_data['to_date'] - cleaned_data['from_date']
        date_from = cleaned_data['from_date']
        user = User.objects.get(id=instance.user.id)
        days_counter = 0
        for day in range(data.days):
            if date_from.isoweekday() == 6 or date_from.isoweekday() == 7:
                date_from = date_from + timedelta(days=1)
                continue
            else:
                days_counter += 1
                date_from = date_from + timedelta(days=1)
        if cleaned_data['status'] == mch.STATUS_CONFIRMED:
            user.vacations_days -= days_counter
            instance.status_changed = datetime.now()
            send_email_async.delay(
                'Request Status',
                'Your request has been confirmed. ' + cleaned_data['reason'],
                user=user.id,
                from_email='bobertestdjango@gmail.com',
                recipient_list=[user.email],
            )
        elif cleaned_data['status'] == mch.STATUS_REJECTED:
            instance.status_changed = datetime.now()
            send_email_async.delay(
                'Request Status',
                'Your request has been rejected. Sorry:) ' + cleaned_data['reason'],
                user=user.id,
                from_email='bobertestdjango@gmail.com',
                recipient_list=[user.email],
            )
        user.save()
        if commit:
            instance.save()
        return instance


class RequestDayOffAdminAddForm(forms.ModelForm):

    class Meta:
        model = RequestDayOffs
        fields = [
            'created', 'from_date', 'to_date', 'reason', 'type', 'user'
        ]


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'age', 'email', 'password', 'salary',
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if User.objects.filter(Q(email=cleaned_data['email']) |
                               Q(username=cleaned_data['email'])).exists():
                raise forms.ValidationError('User already exists')

        return cleaned_data
