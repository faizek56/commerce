from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Categorey,Listing,User,comments,Bid

from .models import User

def listing(request, id):
    listingData=Listing.objects.get(pk=id)
    watchlistis=request.user in listingData.watchlist.all()
    allComments=comments.objects.filter(listing=listingData)
    isOwner=request.user.username == listingData.owner.username
    return render(request,"auctions/listing.html",{
        "list":listingData,
        "watchlistis":watchlistis,
        "comments":allComments,
        "isOwner":isOwner
    })
def closeAuction(request,id):
    listingData=Listing.objects.get(pk=id)
    listingData.isActive=False
    listingData.save()
    isOwner=request.user.username == listingData.owner.username
    watchlistis=request.user in listingData.watchlist.all()
    allComments=comments.objects.filter(listing=listingData)
    return render(request,"auctions/listing.html",{
        "list":listingData,
        "watchlistis":watchlistis,
        "comments":allComments,
        "isOwner":isOwner,
        "message":"Congrats ! your auctions is closed.",
        "update":True
    })
def addbid(request,id):
    newBid=request.POST['newbid']
    listingData=Listing.objects.get(pk=id)
    watchlistis=request.user in listingData.watchlist.all()
    allComments=comments.objects.filter(listing=listingData)
    isOwner=request.user.username == listingData.owner.username
    if int(newBid)>listingData.price.bid:
        updateBid=Bid(user=request.user,bid=int(newBid))
        updateBid.save()
        listingData.price=updateBid
        listingData.save()
        return render(request,"auctions/listing.html",{
        "list":listingData,
        "message":"Congragulations! Bid is updated sucessfully ",
        "update":True,
        "watchlistis":watchlistis,
        "comments":allComments,
        "isOwner":isOwner
    })
    else:
       listingData=Listing.objects.get(pk=id)
       watchlistis=request.user in listingData.watchlist.all()
       return render(request,"auctions/listing.html",{
        "list":listingData,
        "message":"Sorry! Bid  updated failed ",
        "update":False,
         "watchlistis":watchlistis,
        "comments":allComments
    })
      
def addcomment(request,id):
    Current_user=request.user
    listingData=Listing.objects.get(pk=id)
    message=request.POST['newComment']
    
    comment=comments(
        author=Current_user,
        listing=listingData,
        message=message
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addwatchlist(request,id):
    listingData=Listing.objects.get(pk=id)
    user=request.user
    listingData.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
def removewatchlist(request,id):
    listingData=Listing.objects.get(pk=id)
    user=request.user
    listingData.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
def watchlist(request):
    currentuser=request.user
    listing=currentuser.listwatchlist.all()
    return render(request,"auctions/watchlists.html",{
        "lists":listing
    })
def index(request):
    allcatagories=Categorey.objects.all()
    listing=Listing.objects.all()
    return render(request, "auctions/index.html",{
        "categories":allcatagories,
        "Lists":listing
    })
def displayC(request):
    if request.method=="POST":
        cff=request.POST['categorey']
        categorey=Categorey.objects.get(categoreyName=cff)
        allcatagories=Categorey.objects.all()
        listing=Listing.objects.filter(categorey=categorey)
        return render(request, "auctions/index.html",{
        "categories":allcatagories,
        "Lists":listing
        })

def creat(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        price=request.POST.get('price')
        img_url=request.POST.get('img_url')
        categorey_name=request.POST.get('categorey')
        owner=request.user
        categoreyData=Categorey.objects.get(categoreyName=categorey_name)
        bid=Bid(bid=int(price),user=owner)
        bid.save()
        new_listing=Listing(
            title=title,
            description=description,
            price=bid,
            img_url=img_url,
            categorey=categoreyData,
            owner=owner
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        allcatagorey=Categorey.objects.all()
        return render(request,"auctions/creat.html",{
            "catagories":allcatagorey
        })
    
  
    
  
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
