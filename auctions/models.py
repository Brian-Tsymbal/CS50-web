from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    Category = models.CharField(max_length=20)
    Title = models.CharField(max_length=25)
    Description = models.CharField(max_length=150)
    Price = models.PositiveIntegerField()
    PriceInt = models.PositiveIntegerField()
    Image = models.URLField(blank=True, null=True)
    Active = models.BooleanField(default=True)
    Creator = models. ForeignKey(
        User, on_delete=models.CASCADE, default=2)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)
