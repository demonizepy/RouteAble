from django import forms
from .models import House

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

    class Meta:
        model = House
        # Включаем их в общий список отображения
        fields = ['city', 'street', 'number', 'floors', 'elevator', 'elevator_width', 'elevator_length']