from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)
    bio = models.TextField(blank=True)
    def __str__(self): return self.name

class Coloring(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="colorings")  # forbidden to delete author with books
    theme = models.CharField(max_length=50, blank=True)   
    pages = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return f"{self.title} ({self.sku})"

class Pencil(models.Model):
    name = models.CharField(max_length=120)               
    brand = models.CharField(max_length=80, blank=True)
    hardness = models.CharField(max_length=10, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    sku = models.CharField(max_length=50, unique=True)
    def __str__(self): return f"{self.name} ({self.sku})"
