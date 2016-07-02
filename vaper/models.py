# vim:set sw=4 ts=4 et:

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from https://goodcode.io/articles/django-singleton-models/
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            o = cls()
            o.save()
            return o

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
		validators = [
            MinValueValidator(0),
        ],
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

    strength = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
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

###
### BILLING
###
#
# A ledger entry.
#

class Ledger(SingletonModel):
    balance = models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 7)

class LedgerEntry(models.Model):
    description = models.CharField(max_length=256)
    amount = models.DecimalField(
        decimal_places = 2,
        max_digits = 7)
    date = models.DateField()

    ledger = models.ForeignKey(
        Ledger,
        on_delete = models.CASCADE,
        related_name = 'entries',
    )

