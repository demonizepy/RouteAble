from django.db import models
from django.contrib.auth.models import User

# --------------------------------Модели для хранения данных о домах, лифтах, пандусах и их доступности---------------------------------
class Elevator(models.Model):
    condition = models.CharField(max_length=100)
    size_width = models.IntegerField()
    size_length = models.IntegerField()
    
    def __str__(self):
        return self.condition 
    
class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class House(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    street = models.CharField(max_length=500)
    number = models.CharField(max_length=100)
    floors = models.IntegerField()
    elevator = models.ForeignKey(Elevator, on_delete = models.RESTRICT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.street +' '+ self.number
    
class RampType(models.Model):
    title = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.title

class Ramps(models.Model):
    degrees = models.FloatField()
    length = models.FloatField()
    type = models.ForeignKey(RampType, on_delete = models.RESTRICT)

class Availability(models.Model):
    ramps = models.ForeignKey(Ramps, on_delete = models.RESTRICT)
    assistans = models.BooleanField()





