from django.db import models



class Category(models.Model):
    name=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

# Create your models here.
class Product(models.Model):
    category=models.ForeignKey(Category , blank=True , null=True , on_delete=models.SET_NULL)
    name=models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='products/' , blank=True , null=True)

    def __str__(self):
        return self.name


    # python manage.py makemigrations
    # python manage.py migrate