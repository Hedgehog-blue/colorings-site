from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class ColoringBook(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="colorings")
    theme = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1000.00") #Disney colorings are about 1000hryv per one:(
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
class Markers(models.Model):
    name = models.CharField(max_length=120)               
    brand = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
