from django.db import models
from django.urls import reverse


# Create your models here.

#Name of Dataase Table is CustomerDetails and Columns are name and password
class CustomerDetails(models.Model):
    id =models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=16,default='')
    
    def __str__(self):
        return self.name

class ItemDetails(models.Model):
    item = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    
   # def __str__(self):
    #    return str(self.item)

    def item(self):
    	return self.item

    def locate(self):
    	return self.location
    
    def price(self):
    	return self.price		

class Document(models.Model):
    docfile = models.FileField(default='')
    customer = models.ForeignKey(
        CustomerDetails, on_delete=models.CASCADE)
