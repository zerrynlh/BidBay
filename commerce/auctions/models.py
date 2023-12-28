from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    #List of item categories
    categories = [('', 'Select a category'),
                ('1', 'Bedroom') ,
                ('2', 'Living Room'),
                ('3', 'Kitchen'),
                ('4', 'Office'),
                ('5', 'Dining Room'),
                ('6', 'Entertainment'),
                ('7', 'Outdoor'),
                ('8', 'Bathroom'),
                ('9', 'Sports'),
                ('10', 'Auto'),
                ('11', 'Electronics'),
                ('12', 'Clothing'),
                ('13', 'Beauty'),
                ('14', 'Other')]

    seller = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "thisuser")
    itemname = models.CharField(max_length = 64)
    price = models.FloatField()
    description = models.TextField(max_length = 200)
    image = models.URLField(max_length = 200)
    category = models.CharField(max_length = 30, choices = categories)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.itemname

class Bid(models.Model):
    name = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "thebidder")
    bid = models.FloatField()
    #Stops date from being saved every time the object is saved but automically adds time on first entry
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "itembid")

    def __str__(self):
        return f"{self.name}: {self.bid} for {self.item}"

class Comments(models.Model):
    name = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "theusercom")
    comment = models.TextField(max_length = 100)
    #Stops datetime from being saved every time the object is saved but automically adds time on first entry
    thedatetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    item = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "itemcomment")

    def __str__(self):
        return f"{self.name}: {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "watchlist")
    items = models.ManyToManyField(Listing, related_name = "watchlistitem")

    def __str__(self):
        return f"{self.user}: {self.items.all()}"
