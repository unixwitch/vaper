# vim:set sw=4 ts=4 et:

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin

###
### FLAVOUR
###
#
# One flavour from a particular manufacturer.
#

class Manufacturer(models.Model):
    name = models.CharField(max_length = 64)
    
    def __str__(self):
        return self.name

class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
admin.site.register(Manufacturer, ManufacturerAdmin)

class Flavour(models.Model):
    manufacturer = models.OneToOneField(
        Manufacturer,
        on_delete = models.CASCADE,
    )

    flavour = models.CharField(max_length = 64)

    def __str__(self):
        return "{} ({})".format(self.flavour, self.manufacturer)

class FlavourAdmin(admin.ModelAdmin):
    model = Flavour
admin.site.register(Flavour, FlavourAdmin)

###
### FLAVOUR INSTANCE
###
#
# A (flavour, strength) pair, used in recipes.
#

class FlavourInstance(models.Model):
    flavour = models.OneToOneField(
        Flavour,
        on_delete = models.CASCADE,
    )

    strength = models.IntegerField(
		validators = [
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
    )

    recipes = models.ForeignKey(
        'Recipe',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return "{}, {}%".format(self.flavour, self.strength)

class FlavourInstanceInline(admin.TabularInline):
    model = FlavourInstance

###
### RECIPE
###
#
# A list of FlavourInstances that creates a single recipe.
#

class Recipe(models.Model):
    name = models.CharField(max_length = 64)
    def __str__(self):
        return self.name

class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = [ FlavourInstanceInline ]

admin.site.register(Recipe, RecipeAdmin)
