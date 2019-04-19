from django.db import models

# Create your models here.
class Product(models.Model):
	title       = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
#	price       = models.DecimalField(decimal_places=2, max_digits=60)
	summary     = models.TextField(blank=False, null=False)
	featured    = models.BooleanField()

class bed(models.Model):
	#id = models.IntegerField(max_length=4)
	type = models.CharField(max_length=20)
	path = models.CharField(max_length=100)


	def _str_(self):
		return self.path

'''from django.db import models

# Create your models here.

#Name of Dataase Table is CustomerDetails and Columns are name and password
class CustomerDetails(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    
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
      return self.price    '''
