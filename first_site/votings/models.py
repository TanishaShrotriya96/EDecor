from django.db import models
from django.urls import reverse
# Create your models here.

#Name of Database Table is CustomerDetails and Columns are name and password.
class CustomerDetails(models.Model):
    id =models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=16,default='')
    
    def __str__(self):
        return self.name

    def id(self):
        return self.id

#Table created for storing details of items, not currently in use.
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

#Table stores image of user's room and foreign key to username.
#Future scope to integrate google drive API.
class Document(models.Model):

    docfile = models.FileField(default='')
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    style1=models.CharField(default='',max_length=100)
    style2=models.CharField(default='',max_length=100)
  
#Category of furniture items like Bed, Table, Chair and so on.
class Category(models.Model):
    #db_index = True added to optimize searches through the database.
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('votings:product_list_by_category', args=[self.slug]) #reverse() is used to go back to same page.

#Products specific to each furniture item.

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('votings:product_detail', args=[self.id, self.slug])

