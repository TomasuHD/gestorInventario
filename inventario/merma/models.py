from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name

class ItemInventario(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    provider = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, blank=True, null=True)
    entry_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name