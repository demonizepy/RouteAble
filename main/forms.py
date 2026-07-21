from django import forms
from .models import House, Availability


class HouseForm(forms.ModelForm):
    availability = forms.ModelChoiceField(
        label="Доступность",
        queryset=Availability.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'id_availability'})
    )

    class Meta:
        model = House
        fields = [
            'city', 
            'street', 
            'number', 
            'floors', 
            'has_elevator', 
            'elevator_width', 
            'elevator_length', 
            'has_ramp', 
            'ramp_degrees', 
            'ramp_length', 
            'availability'
        ]
        widgets = {
            'city': forms.TextInput(attrs={'id': 'id_city', 'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'id': 'id_street', 'placeholder': 'Улица'}),
            'number': forms.TextInput(attrs={'id': 'id_number', 'placeholder': 'Номер дома'}),
            'floors': forms.NumberInput(attrs={'id': 'id_floors', 'min': '1'}),
            
            'has_elevator': forms.CheckboxInput(attrs={'id': 'id_has_elevator'}),
            'elevator_width': forms.NumberInput(attrs={'id': 'id_elevator_width', 'min': '0', 'placeholder': 'см'}),
            'elevator_length': forms.NumberInput(attrs={'id': 'id_elevator_length', 'min': '0', 'placeholder': 'см'}),
            
            'has_ramp': forms.CheckboxInput(attrs={'id': 'id_has_ramp'}),
            'ramp_degrees': forms.NumberInput(attrs={'id': 'id_ramp_degrees', 'step': '0.1', 'min': '0', 'placeholder': 'градусы'}),
            'ramp_length': forms.NumberInput(attrs={'id': 'id_ramp_length', 'step': '0.1', 'min': '0', 'placeholder': 'метры'}),
        }