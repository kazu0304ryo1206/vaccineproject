from django.db import models
from django.contrib.auth.models import AbstractUser

class PlaceModel(models.Model):
    place = models.CharField(max_length=50)
    images = models.ImageField(upload_to='')
    def __str__(self):
        return self.place

class CalendarModel(models.Model):
    day = models.CharField(max_length=20)
    def __str__(self):
        return self.day

class TimeModel(models.Model):
    time = models.CharField(max_length=20)
    def __str__(self):
        return self.time
        
class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass
    address = models.CharField(max_length=50)
    age = models.IntegerField('年齢',blank=True,null=True)
    zip_code = models.CharField(max_length=10)

class RegisterModel(models.Model):
    place = models.ForeignKey(PlaceModel,on_delete=models.CASCADE)
    day = models.ForeignKey(CalendarModel,on_delete=models.CASCADE)
    time = models.ForeignKey(TimeModel,on_delete=models.CASCADE)
    username = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    check = models.BooleanField()
    


