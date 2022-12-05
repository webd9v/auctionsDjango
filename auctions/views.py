from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from datetime import date
from .models import User, AuctionItem, Bid, Comment, Category
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "auctions/index.html",{
        "items":AuctionItem.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user=authenticate(request,username=username,password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def addListing(request):
    if request.method=="POST":
        name=request.POST["name"]
        baseprice=int(request.POST["baseprice"])
        desc=request.POST["description"]
        duration=request.POST["duration"]
        duration=duration.split("-")
        enddate=datetime.date(int(duration[0]),int(duration[1]),int(duration[2]))
        bid_startdate=date.today()
        if enddate<bid_startdate:
            return render(request,"auctions/add_listing.html",{
                "categories":Category.objects.all(),
                "message":"The date entered is before today!"
            })
        image=request.FILES["image"]
        cat=int(request.POST["category"])
        instance=AuctionItem.objects.create(name=name,user=User.objects.get(pk=request.user.id),baseprice=baseprice,description=desc,image=image,category=Category.objects.get(pk=cat),bid_startdate=bid_startdate,bid_enddate=enddate)
        id=instance.pk
        return HttpResponseRedirect(reverse("auctions:listing",args=(id,)))
    return render(request,"auctions/add_listing.html",{
        "categories":Category.objects.all(),
    })

@login_required()
def displayListing(request,id):
    item=AuctionItem.objects.get(pk=id)
    today=date.today()
    isFinished=False
    if today>item.bid_enddate and item.winner is not None:
        item.winner=item.highest_bidder
        item.save()
        isFinished=True
    bids=item.bids.all()
    comments=item.listingcomments.all()
    isWatched=request.user.watchlist.filter(pk=AuctionItem.objects.get(pk=id).pk).exists()
    return render(request,"auctions/single_listing.html",{
        "item":item,
        "bids":bids,
        "comments":comments,
        "isFinished":isFinished,
        "isWatched":isWatched
    })

@login_required
def addComment(request):
    if request.method=="POST":
        content=str(request.POST["content"])
        userid=request.user.id
        next=int(request.POST["next"])
        today=date.today()
        comment=Comment.objects.create(user=User.objects.get(pk=userid),content=content,dateposted=today,auctionitem=AuctionItem.objects.get(pk=next))
        comment.save()
        return HttpResponseRedirect(reverse("auctions:listing",args=(next,)))
    else:
        return HttpResponseRedirect(reverse("auctions:index"))

@login_required
def addBid(request):
    if request.method=="POST":
        user=request.user.id
        inputAmount=request.POST["amount"]
        if not inputAmount:
            inputAmount=0
        amount=int(inputAmount)
        next=int(request.POST["next"])
        item=AuctionItem.objects.get(pk=next)
        if item.baseprice>amount:
            today=date.today()
            isFinished=False
            if today>item.bid_enddate and item.winner is not None:
                item.winner=item.highest_bidder
                item.save()
                isFinished=True
            bids=item.bids.all()
            comments=item.listingcomments.all()
            return render(request,"auctions/single_listing.html",{
                "item":item,
                "bids":bids,
                "comments":comments,
                "isFinished":isFinished,
                "bidmessage":"Amount is less then the base price!"
            })
        today=date.today()
        bid=Bid.objects.create(user=User.objects.get(pk=user),amount=amount,auctionitem=item,date_placed=today)
        item=AuctionItem.objects.get(pk=next)
        if amount>item.highest_bid:
            item.highest_bid=amount
            item.highest_bidder=User.objects.get(pk=request.user.id)
            item.save()
        bid.save()
        return HttpResponseRedirect(reverse("auctions:listing",args=(next,)))
    else:
        return HttpResponseRedirect(reverse("auctions:index"))

def displayWatchList(request):
    print(request.user.watchlist)
    return render(request,"auctions/watchlist.html",{
        "watchlist":request.user.watchlist.all(),
    })

def displayItemsByCategory(request):
    if request.method=="POST":
        id=int(request.POST["category"])
        if id==-1:
            return render(request,"auctions/categories.html",{
                "cats":Category.objects.all(),
                "items":AuctionItem.objects.all(),
                "selectedid":None
            })
        cat=Category.objects.get(pk=id)
        return render(request,"auctions/categories.html",{
            "cats":Category.objects.all(),
            "items":cat.cat_items.all(),
            "selectedid":id
        })
    return render(request,"auctions/categories.html",{
        "cats":Category.objects.all(),
        "items":AuctionItem.objects.all(),
        "selectedid":None
    })
@login_required
def toggleItemInWatchlist(request,item_id):
    item=AuctionItem.objects.get(pk=item_id)
    if item.savedby.filter(pk=request.user.id).exists():
        item.savedby.set(item.savedby.exclude(pk=request.user.id))
    else:
        item.savedby.add(User.objects.get(pk=request.user.id))
    return HttpResponseRedirect(reverse("auctions:listing",args=(item_id,)))
