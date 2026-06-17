from django import forms
from .models import House, Elevator, Ramps, Availability

class HouseForm(forms.ModelForm):
    # Добавляем кастомные поля, которых нет в модели House
    elevator_width = forms.IntegerField(
        label="Ширина лифта (см)", 
        required=False, 
        widget=forms.NumberInput(attrs={'id': 'id_elevator_width', 'min': '0'})
    )
    elevator_length = forms.IntegerField(
        label="Длина лифта (см)", 
        required=False, 
        widget=forms.NumberInput(attrs={'id': 'id_elevator_length', 'min': '0'})
    )
    ramps = forms.ModelChoiceField(
        label="Пандус",
        queryset=Ramps.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'id_ramps'})
    )
    ramp_degrees = forms.FloatField(
        label="Угол наклона пандуса (°)",
        required=False,
        widget=forms.NumberInput(attrs={'id': 'id_ramp_degrees', 'step': '0.1', 'min': '0'})
    )
    ramp_length = forms.FloatField(
        label="Длина пандуса (м)",
        required=False,
        widget=forms.NumberInput(attrs={'id': 'id_ramp_length', 'step': '0.1', 'min': '0'})
    )    
    availability = forms.ModelChoiceField(
        label="Доступность",
        queryset=Availability.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'id_availability'})
    )

    class Meta:
        model = House
        # Включаем их в общий список отображения
        fields = ['city', 'street', 'number', 'floors', 'elevator', 'elevator_width', 'elevator_length', 'ramps', 'ramp_degrees', 'ramp_length', 'availability']