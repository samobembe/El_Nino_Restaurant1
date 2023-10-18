from django.db import models
# from django.contrib.auth.admin import 
from django.db.models import Avg

# Create your models here.

# Represents a single ingredient in the inventory 
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=6, decimal_places=1)
    unit = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

# Represents entry on the menu for the restaurant
class MenuItem(models.Model):                                       
    title = models.CharField(max_length=300, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    def __str__(self):
        return f"{self.title}: {self.price}- {self.average_rating()}"

# Represents an ingredient required for a recipe required for a Menu Item
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)

# Represents a customer purchase of an item off the menu.
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# A rating system for each of the the items on the menu
class Rating(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.header}: {self.rating}"