from django.db import models
# from django.contrib.auth.admin import 
from django.db.models import Avg

# Create your models here.

# Represents an entry off the restaurant's menu
class MenuItem(models.Model):
    title = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0.00)

    def get_absolute_url(self):
        return "/menu"
    
    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    def __str__(self):
        return f"title={self.title}; price={self.price}"
    
    # Rating metrics
    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.header}: {self.average_rating()}"

# Rating model
class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.header}: {self.rating}"


# Represents a single ingredient in the restaurant's inventory
class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=200)
    price_per_unit = models.FloatField(default=0)

    def get_absolute_url(self):
        return "/ingredients"
    

    def __str__(self):
        return f"""
        name={self.name};
        qty={self.quantity};
        unit={self.unit};
        unit_price={self.price_per_unit}
        """


# Represents an ingredient required for a recipe for a MenuItem
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}]; ingredient={self.ingredient.name}; qty={self.quantity}"
    
    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity <= self.ingredient.quantity


#Represents a purchase off a MenuItem
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}]; time={self.timestamp}"

    def get_absolute_url(self):
        return "/purchases"
