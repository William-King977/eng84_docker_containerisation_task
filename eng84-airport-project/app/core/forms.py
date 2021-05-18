from django import forms
from django.forms.models import ModelForm
# from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# from crispy_forms.layout import Submit, Layout, Div, Fieldset
from bootstrap_datepicker_plus import DateTimePickerInput, TimePickerInput, DatePickerInput

from .models import Flight, Aircraft, Passenger, Staff, Airport


class FlightsForm(forms.ModelForm):
    connection = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=Airport.objects.exclude(id__exact=1))
    crew = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                  queryset=Staff.objects.filter(role__in=["PILOT", "FLIGHT ATTENDANT"]),
                                  required=False
                                  )

    class Meta:
        model = Flight
        fields = ('flight_type', 'connection', 'departure_time', 'aircraft_id', 'crew', 'attendance')

        widgets = {
                'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stansted'}),
                'destination': forms.TextInput(attrs={'class': 'form-control'}),
                'departure_time': DateTimePickerInput(),
                'duration': TimePickerInput(attrs={'class': 'form-control'}),
                'aircraft_id': forms.Select(attrs={'class': 'form-control'}),
                'attendance': forms.SelectMultiple(attrs={'class': 'form-control'}),
                'flight_type': forms.Select(attrs={'class': 'form-control'}),
                }


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ('first_name', 'last_name', 'dob', 'passport_num')

        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', }),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'dob': DatePickerInput(attrs={'label': 'Date of Birth'}),
                'passport_num': forms.TextInput(attrs={'class': 'form-control'}),
                }
        labels = {
                'dob': _('Date of Birth'),
                'passport_num': _('Passport Number')
                }


class StaffForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff 
        fields = ('first_name', 'last_name', 'dob', 'email',  'role', 'password', 'password_confirm')


        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', }),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.EmailInput(attrs={'class': 'form-control'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                'dob': DatePickerInput(attrs={'label': 'Date of Birth'}),
                'role': forms.Select(attrs={'class': 'form-control'}),
                }

        labels = {
                'dob': _('Date of Birth'),
                }

    def clean(self, *args, **kwargs):
        data = super().clean()
        password1 = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password_confirm', None)

        if password1 and password2:
            if password1 == password2:
                return data
            else:
                raise forms.ValidationError(_('Passwords do not match'))
            return data
        else:
            raise ValidationError(_('Password field is empty'))
        return None



class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ('name', 'city', 'country', 'distance')

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control' }),
                'city': forms.TextInput(attrs={'class': 'form-control'}),
                'country': forms.TextInput(attrs={'class': 'form-control'}),
                'distance': forms.NumberInput(attrs={'class': 'form-control'}),
                }


class AircraftForm(forms.ModelForm):
    class Meta:
        model = Aircraft 
        fields = ('model', 'manufacturer', 'capacity', 'weight')

        widgets = {
                'model': forms.TextInput(attrs={'class': 'form-control' }),
                'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
                'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
                'weight': forms.NumberInput(attrs={'class': 'form-control'}),
                }

# class StaffForm(forms.ModelForm):
#     class Meta:
#         model = Staff 
#         fields = ('first_name', 'last_name', 'dob', 'email', 'role', 'password')
# 
#         widgets = {
#                 'email': forms.EmailInput(attrs={'class': 'form-control'}),
#                 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#                 'first_name': forms.TextInput(attrs={'class': 'form-control', }),
#                 'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#                 'dob': DatePickerInput(),
#                 'role': forms.TextInput(attrs={'class': 'form-control'}),
# 
#                 }
# 
#         labels = {
#                 'dob': _('Date of Birth'),
#                 }
