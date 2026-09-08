from django import forms
from .models import Plant, CareLog


class PlantForm(forms.ModelForm):
    """ Form for creating and updating Plant instances. """

    acquired_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control', 'type': 'date'},
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Plant
        fields = [
            'nickname',
            'species',
            'location',
            'acquired_date',
            'water_frequency_days',
            'light_needs',
            'notes',
        ]
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'water_frequency_days': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}
            ),
            'light_needs': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
        }


class CareLogForm(forms.ModelForm):
    """ Form for creating and updating CareLog instances. """

    date = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control', 'type': 'date'},
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = CareLog
        fields = ['date', 'action', 'notes']
        widgets = {
            'action': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
