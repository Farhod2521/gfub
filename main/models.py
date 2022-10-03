from django.db import models

# Create your models here.
class Chat_ID(models.Model):
    chat_id  =  models.PositiveBigIntegerField()
# Sample User model
class Malumotlar(models.Model):
    full_name = models.CharField(max_length=500)
    phone =  models.CharField(max_length=500)
    who =  models.CharField(max_length=500)
    bolim =  models.CharField(max_length=500)
    kimga =  models.CharField(max_length=500)
    text = models.TextField()
    chat_id  =  models.PositiveBigIntegerField()
    data = models.DateField(auto_now= True)



    def __str__(self):
        return self.full_name