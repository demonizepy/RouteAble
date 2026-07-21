from rest_framework import serializers
from .models import House, Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('id', 'assistance')


class HouseSerializer(serializers.ModelSerializer):
    availability = AvailabilitySerializer(read_only=True)

    class Meta:
        model = House
        fields = (
            'id', 
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
            'availability', 
            'latitude', 
            'longitude'
        )
        
# -------------------------------Сериализатор для модели House для обработки запросов к API---------------------------------
# class HouseModel: # локальные переменные для передачи данных в формате JSON, не связаны с моделью House в models.py
#     def __init__(self, id, city, street, number, floors, elevator_id, latitude, longitude):
#         self.id = id
#         self.city = city
#         self.street = street
#         self.number = number
#         self.floors = floors
#         self.elevator_id = elevator_id
#         self.latitude = latitude
#         self.longitude = longitude
        
        
# --------------------------------Примеры сериализации и десериализации для наглядного объяснения процесса---------------------------------        
# class HouseSerializer(serializers.Serializer): # преобразование в словарь для передачи данных в формате JSON и обратно, 
#                                                 # определение полей и их типов данных для сериализации и десериализации
#     id = serializers.IntegerField(max_value=1000000)
#     city = serializers.CharField(max_length=100)
#     street = serializers.CharField(max_length=100)
#     number = serializers.CharField(max_length=10)
#     floors = serializers.IntegerField(max_value=100)
#     elevator_id = serializers.IntegerField()
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()
    
#     def create(self, validated_data): # создание нового объекта House на основе проверенных данных
#         return House.objects.create(**validated_data)

#     def update(self, instance, validated_data): # обновление существующего объекта House на основе проверенных данных
#         instance.city = validated_data.get('city', instance.city)
#         instance.street = validated_data.get('street', instance.street)
#         instance.number = validated_data.get('number', instance.number)
#         instance.floors = validated_data.get('floors', instance.floors)
#         instance.elevator_id = validated_data.get('elevator_id', instance.elevator_id)
#         instance.latitude = validated_data.get('latitude', instance.latitude)
#         instance.longitude = validated_data.get('longitude', instance.longitude)
#         instance.save()
#         return instance

# def encode(): # наглядное объяснение процесса сериализации, создание объекта HouseModel, преобразование его в словарь с помощью HouseSerializer и затем в JSON формат с помощью JSONRenderer
#     model = HouseModel(1, 'Moscow', 'Lenina', '10', 5, 1, 55.7558, 37.6173)
#     model_sr = HouseSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')    
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
    
# def decode(): # наглядное объяснение процесса десериализации, преобразование JSON формата обратно в словарь с помощью JSONParser и затем в объект HouseModel с помощью HouseSerializer
#     stream = io.BytesIO(b'{"id": 1, "city": "Moscow", "street": "Lenina", "number": "10", "floors": 5, "elevator_id": 1, "latitude": 55.7558, "longitude": 37.6173}')
#     data = JSONParser().parse(stream)
#     serializer = HouseSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
