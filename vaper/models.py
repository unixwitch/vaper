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
    name = models.CharField(max_length = 64, unique=True)

    def __str__(self):
        return self.name

class ManufacturerInline(admin.TabularInline):
    model = Manufacturer

class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer

admin.site.register(Manufacturer, ManufacturerAdmin)

class Flavour(models.Model):
    class Meta:
        unique_together = ('name', 'manufacturer', )

    name = models.CharField(max_length = 64)

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete = models.CASCADE,
        related_name = 'flavours',
    )

    ml_remaining = models.PositiveIntegerField(
        verbose_name = 'Remaining (ml)'
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.manufacturer)

class FlavourInline(admin.TabularInline):
    model = Flavour

class FlavourAdmin(admin.ModelAdmin):
    model = Flavour

admin.site.register(Flavour, FlavourAdmin)

###
### RECIPE
###
#
# A list of FlavourInstances that creates a single recipe.
#

class Recipe(models.Model):
    name = models.CharField(max_length = 64, unique=True)

    description = models.TextField(
        null = True,
		blank = True,
    )

    def __str__(self):
        return self.name


###
### FLAVOUR INSTANCE
###
#
# A (flavour, strength) pair, used in recipes.
#

class FlavourInstance(models.Model):
    class Meta:
        verbose_name_plural = "Flavours"

    flavour = models.ForeignKey(
        Flavour,
        on_delete = models.CASCADE,
        related_name = 'flavour_instances'
    )

    strength = models.IntegerField(
		validators = [
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
    )

    recipes = models.ForeignKey(
        Recipe,
        on_delete = models.CASCADE,
        related_name = 'flavour_instances',
    )

    def __str__(self):
        return "{}, {}%".format(self.flavour, self.strength)

class FlavourInstanceInline(admin.TabularInline):
    model = FlavourInstance
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = [ FlavourInstanceInline ]

admin.site.register(Recipe, RecipeAdmin)

