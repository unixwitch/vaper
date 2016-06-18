# vim:set sw=4 ts=4 et:

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Flavour(models.Model):
    class Meta:
        unique_together = ('name', 'manufacturer', )

    name = models.CharField(max_length = 64)

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete = models.CASCADE,
        related_name = 'flavours',
    )

    ml = models.DecimalField(
        verbose_name = 'Remaining (ml)',
        max_digits = 7,
        decimal_places = 2,
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.manufacturer)

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
