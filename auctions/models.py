from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(verbose_name="Category",max_length=100,blank=False,null=False,unique=True)

class AuctionItem(models.Model):
    name=models.CharField(verbose_name="Item's Name",max_length=250,null=False,blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="items",null=False,blank=False,verbose_name="Owner")
    baseprice=models.IntegerField(verbose_name="Starting Price")
    description=models.CharField("Description",max_length=500,null=False,blank=False)
    image=models.FileField(verbose_name="Item's Image")
    bid_startdate=models.DateField("Start date of this auction")
    bid_enddate=models.DateField("Auction's End Date")
    highest_bid=models.IntegerField(verbose_name="Highest Bid",default=0)
    highest_bidder=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    savedby=models.ManyToManyField(User,blank=True,null=True,related_name="watchlist")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="cat_items")
    winner=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="items_won",blank=True,null=True)

class Bid(models.Model):
    user=models.ForeignKey(User, verbose_name="Bidder's Name", on_delete=models.CASCADE,related_name="offers")
    amount=models.IntegerField()
    date_placed=models.DateField("Date Placed")
    auctionitem=models.ForeignKey(AuctionItem, verbose_name="Auction Item", on_delete=models.CASCADE,related_name="bids")

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    dateposted=models.DateField()
    content=models.CharField(max_length=500)
    auctionitem=models.ForeignKey(AuctionItem,on_delete=models.CASCADE,related_name="listingcomments")
