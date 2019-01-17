#from django.forms import ModelForm
from django import forms
from django.db.models import Q
from datetime import timedelta

from apps.account.models import User, ContactUs, RequestDayOffs




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
            'type', 'from_date', 'to_date',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        from pdb import set_trace
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['from_date'] > cleaned_data['to_date']:
                self.add_error('to_date', 'from_date cannot be greater then to_date')
            data = cleaned_data['to_date'] - cleaned_data['from_date']
            if cleaned_data["type"] == 3 and data.days > 1:
                self.add_error('to_date', 'dayoff should be not more then 1 day')
            date_from = cleaned_data['from_date']
            maximum = 0
            for day in range(data.days):
                if date_from.isoweekday() == 6 or date_from.isoweekday() == 7:
                    date_from = date_from + timedelta(days=1)
                    continue
                else:
                    maximum += 1
                    date_from = date_from + timedelta(days=1)
            if maximum >= 20:
                self.add_error('type', "vacation shouldn't be less then 20 working days")
            if maximum > self.user.vacations_days:
                self.add_error('type', "you have not enough days to get this vacation")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance








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
