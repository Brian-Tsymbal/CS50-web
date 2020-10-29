from django import forms
from django.forms import ModelForm


from django.db import IntegrityError
from django.db.models import Avg, Max, Min, Sum

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import User
from .models import Listings
from .models import Watchlist
from .models import Comments
from .models import Bids

choices = [
    ("Technology", "Technology"),
    ("Tools", "Tools"),
    ("Toys", "Toys"),
    ("Fashion", "Fashion")
]


# to do:

# Forms
class CategoriesForm(forms.Form):
    CATEGORY = forms.ChoiceField(choices=choices)


class BiddingForm(forms.Form):
    Bid = forms.IntegerField()


class AddComment(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))


class ClosingForm(forms.Form):
    Close = forms.BooleanField(label="Close This Form")


class WatchlistForm(forms.Form):
    AddWatchlist = forms.BooleanField(label="Add this page ")


class RemoveWatchlist(forms.Form):
    RemoveItem = forms.BooleanField(label="Remove from Watchlist")

# Page functions


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listings.objects.all(),

    })


def Creating_listing(request):
    if request.method == 'POST':
        categories = request.POST['Categories']
        title = request.POST['Title']
        description = request.POST['Description']
        value = request.POST['Value']
        image = request.POST['Image']
        active = True
        Listing = Listings(Category=categories, Title=title,
                           Description=description, Price=value, PriceInt=value, Image=image, Active=active, Creator=request.user)
        Listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {})


def Categories(request):
    if request.method == 'POST':
        FormResult = CategoriesForm(request.POST)
        if FormResult.is_valid():
            entries = FormResult.cleaned_data['CATEGORY']
            category = FormResult.cleaned_data['CATEGORY']
            entries = Listings.objects.filter(Category=entries)
            return render(request, "auctions/Categories.html", {
                "listings": Listings.objects.filter(Category=category),
                "entries": entries,
                "form": FormResult
            })
        else:
            return render(request, "auctions/Categories.html", {
                "form": FormResult
            })
    else:
        return render(request, "auctions/Categories.html", {
            "form": CategoriesForm()
        })


def GeneralView(request, name):
    if request.method == 'POST':
        Creator = Listings.objects.get(pk=name).Creator
        if request.user == Creator:
            Commenting(request, name)
            Closing(request, name)
        else:
            Commenting(request, name)
            RemoveWatchlistItem(request, name)
            NewWatchlistItem(request, name)
        return HttpResponseRedirect(reverse("listing", args=[name]))
    else:
        if Listings.objects.get(pk=name).Price != Listings.objects.get(pk=name).PriceInt:
            MaxBid = Listings.objects.get(pk=name).Price
            Highestbidder = Bids.objects.get(item=name, value=MaxBid).user
        else:
            Highestbidder = Listings.objects.get(pk=name).Creator
        return render(request, "auctions/general.html", {
            "item":  Listings.objects.get(pk=name),
            "comments": Comments.objects.filter(item=Listings.objects.get(pk=name)),
            "commentForm": AddComment(),
            "HighestBidder": Highestbidder,
            "ClosingForm": ClosingForm(),
            "WatchlistForm": WatchlistForm(),
            "RemoveItem": RemoveWatchlist(),
            "Watchlist": Watchlist.objects.filter(user=request.user, item=Listings.objects.get(pk=name))
        })


def WatchlistPage(request):
    return render(request, "auctions/Watchlist.html", {
        "list": Watchlist.objects.filter(user=request.user),
        "WatchlistChoices": Listings.objects.all()
    })


# Auction functions

def NewWatchlistItem(request, item):
    WatchlistResults = WatchlistForm(request.POST)
    if WatchlistResults.is_valid():
        item = Listings.objects.get(pk=item)
        NewItem = Watchlist(user=request.user, item=item)
        NewItem.save()


def RemoveWatchlistItem(request, item):
    Remove = RemoveWatchlist(request.POST)
    if Remove.is_valid():
        ItemId = Watchlist.objects.get(user=request.user, item=item).id
        Delete = Watchlist.objects.filter(pk=ItemId).delete()


def Biding(request, item):
    if request.method == 'POST':
        FormSubmit = BiddingForm(request.POST)
        if FormSubmit.is_valid():
            bid = FormSubmit.cleaned_data['Bid']
            user = request.user
            if bid > Listings.objects.get(pk=item).Price:
                NewBid = Bids(
                    user=user, item=Listings.objects.get(pk=item), value=bid)
                NewBid.save()
                Update = Listings.objects.filter(pk=item).update(Price=bid)
                return HttpResponseRedirect(reverse("listing", args=item))
            else:
                return render(request, "auctions/Biding.html", {
                    "form": BiddingForm(),
                    "item": Listings.objects.get(pk=item),
                    "error": f"Your Bid must be above ${Listings.objects.get(pk=item).Price} on Item:{item}"
                })
    else:
        return render(request, "auctions/Biding.html", {
            "form": BiddingForm(),
            "item": Listings.objects.get(pk=item)
        })


def Commenting(request, ITEM):
    FormResult = AddComment(request.POST)
    if FormResult.is_valid():
        comment = FormResult.cleaned_data['comment']
        item = Listings.objects.get(pk=ITEM)
        user = request.user
        NewComment = Comments(user=user, item=item, comment=comment)
        NewComment.save()


def Closing(request, page):
    ClosingResults = ClosingForm(request.POST)
    if ClosingResults.is_valid():
        Closed = False
        ClosingPage = Listings.objects.filter(pk=page).update(Active=Closed)


# Header functions


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
