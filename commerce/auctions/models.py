from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categorey(models.Model):
    categoreyName=models.CharField(max_length=200)

    def __str__(self):
        return self.categoreyName
    

class Bid(models.Model):
    bid=models.IntegerField(default=0)
    user=models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE,related_name="userbid")

    def __str__(self):
        return f"{self.user.username} bid {self.bid}"

class Listing(models.Model):
    title=models.CharField(max_length=44)
    description=models.CharField(max_length=300)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,blank=True,null=True,related_name="bidprice")
    img_url=models.CharField(max_length=30000)
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE,related_name="user")
    categorey=models.ForeignKey(Categorey,blank=True,null=True,on_delete=models.CASCADE,related_name="categorey")
    watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="listwatchlist")
    def __str__(self):
        return self.title
    
class comments(models.Model):
    author=models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE,related_name="userComment")
    listing=models.ForeignKey(Listing,blank=True,null=True, on_delete=models.CASCADE,related_name="listingData")
    message=models.CharField(max_length=1000)
    def __str__(self):
        return f"{self.author} comment on {self.listing}"
       
