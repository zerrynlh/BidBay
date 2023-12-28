from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Bid, Comments, Watchlist

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

#List of item categories
filters = [('0', 'All Categories'),
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

class ListingForm(forms.Form):
    thetitle = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter a title', 'class' : 'form-control'}))
    thedescription = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder': 'Enter text here...', 'class' : 'form-control'}))
    theprice = forms.FloatField(label="Starting Bid", widget=forms.NumberInput(attrs={'placeholder': 'Enter a price', 'class' : 'form-control', 'min' : '0.00' }))
    thepicture = forms.URLField(label="Image URL", widget=forms.URLInput(attrs={'placeholder': 'Enter a URL ', 'class' : 'form-control'}))
    thecategory = forms.ChoiceField(label="Category", choices = categories, widget=forms.Select(attrs={'class' : 'form-control'}))

class BidForm(forms.Form):
    thebid = forms.FloatField(label="Place Bid", widget=forms.NumberInput(attrs={'placeholder' : 'Ex: 5.00', 'class' : 'form-control', 'min' : '0.00', 'name' : 'place_bid'}))

class CommentForm(forms.Form):
    thecomment = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Type your comment...', 'class' : 'form-control', 'max_length' : '200', 'rows' : '5', 'name' : 'add_comment'}))

class FilterForm(forms.Form):
    thefilter = forms.ChoiceField(choices = filters, widget=forms.Select(attrs={'class' : 'form-control', 'style' : 'width: 30vh;'}))


@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        filter = FilterForm(request.POST)
        if filter.is_valid():
            userfilter = filter.cleaned_data["thefilter"]

        if userfilter == '0':
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index") + f"?filter={userfilter}")

    if request.method == "GET":
        userfilter = request.GET.get('filter', None)

        #Sorts listings in descending order by date
        #If the filter is at index 0, all listings are rendered
        #Otherwise, a filter is applied
        if userfilter == '0' or userfilter == None:
            filter = FilterForm()
            listings = Listing.objects.all().order_by('-date')
        else:
            filter = FilterForm(initial={'thefilter': f'{userfilter}'})
            listings = Listing.objects.filter(category=userfilter).order_by('-date')
            
        return render(request, "auctions/index.html", {
            "listings" : listings,
            "filter" : filter
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

@login_required(login_url="/login")
def create(request):
    if request.method == "GET":
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "form" : form
        })
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            theseller = request.user
            thetitle = form.cleaned_data["thetitle"]
            thedescription = form.cleaned_data["thedescription"]
            theprice = form.cleaned_data["theprice"]
            thepicture = form.cleaned_data["thepicture"]
            thecategory = form.cleaned_data["thecategory"]

            #Creates new listing to be stored
            new_listing = Listing(
                seller = theseller,
                itemname=thetitle,
                description=thedescription,
                price=round(theprice, 2),
                image=thepicture,
                category=thecategory

            )

            #Listing is stored in database
            new_listing.save()

            #Redirects user back to homepage once listing is created
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html", {
                "form" : form
            })

@login_required(login_url="/login")
def listing(request, item):
    #Gets primary ID of listing
    item = Listing.objects.get(pk=int(item))

    #Comments are sorted in descending order
    comments = Comments.objects.all().order_by('-thedatetime')

    bid_form = BidForm()
    comment_form = CommentForm()

    #Checks if user has a watchlist. If not, a watchlist is created
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    #Sets variables to check if the item is already in the user's watchlist
    in_watchlist = False
    watchlist_items = watchlist.items.all()
    watchlist_items = [items.id for items in watchlist_items]
    if item.id in watchlist_items:
        in_watchlist = True

    #Gets and displays any current bids
    try:
        current_bids = Bid.objects.filter(item=item).order_by('-date')
    except ObjectDoesNotExist:
        current_bids = None

    #Status of auction
    status = item.is_closed

    #Gets winner if one exists
    thewinner = item.winner

    message = ""

    #Message to display if the listing is closed
    if status == True:
        if request.user != thewinner:
            message = "This listing has been closed."
        else:
            message = "Congratulations, you have won this auction! \U0001F389"

    if request.method == "GET":
        bid_form = BidForm()
        comment_form = CommentForm()
        return render(request, "auctions/listing.html", {
            "item" : item,
            "bid_form" : bid_form,
            "com_form" : comment_form,
            "comments" : comments,
            "in_watchlist" : in_watchlist,
            "current_bids" : current_bids,
            "is_closed" : status,
            "winner" : thewinner,
            "message" : message

        })

    if request.method == "POST":
        if 'add_watchlist' in request.POST:
            watchlist_id = request.POST["listing_id"]
            watcher = request.user

            #Gets ID of listing
            thelisting = Listing.objects.get(pk=int(watchlist_id))

            #Checks if user has a watchlist. If not, a watchlist is created
            watchlist, created = Watchlist.objects.get_or_create(user=watcher)

            #If the item is not in the watchlist, it is added. Otherwise, it is removed
            if not in_watchlist:
                watchlist.items.add(thelisting)
                in_watchlist = True

                return render(request, "auctions/listing.html", {
                        "item" : item,
                        "bid_form" : bid_form,
                        "com_form" : comment_form,
                        "comments" : comments,
                        "current_bids" : current_bids,
                        "message" : "Item was successfully added to your watchlist!",
                        "in_watchlist" : in_watchlist,
                        "is_closed" : status,
                        "winner" : thewinner
                    })

            else:
                watchlist.items.remove(thelisting)
                in_watchlist = False

                return render(request, "auctions/listing.html", {
                        "item" : item,
                        "bid_form" : bid_form,
                        "com_form" : comment_form,
                        "comments" : comments,
                        "current_bids" : current_bids,
                        "message" : "Item was removed from your watchlist.",
                        "in_watchlist" : in_watchlist,
                        "is_closed" : status,
                        "winner" : thewinner
                    })


        if 'thebid' in request.POST:
            placebid_form = BidForm(request.POST)

            if placebid_form.is_valid():
                bid = placebid_form.cleaned_data["thebid"]
                user = request.user
                date = datetime.now().date()
                theitem = Listing.objects.get(pk=item.id)

                itemprice = item.price

                #Checks if the user's bid is higher than the starting price
                if bid < itemprice:
                    return render(request, "auctions/listing.html", {
                    "item" : item,
                    "bid_form" : bid_form,
                    "com_form" : comment_form,
                    "comments" : comments,
                    "in_watchlist" : in_watchlist,
                    "current_bids" : current_bids,
                    "message" : f"Your bid of ${bid:,.2f} is less than the starting bid of ${itemprice:,.2f}.",
                    "is_closed" : status,
                    "winner" : thewinner
                })

                #Attempts to collect any current bids associated with the listing
                try:
                    current_bids = Bid.objects.filter(item=item)
                except ObjectDoesNotExist:
                    current_bids = None

                user_bids = []

                #If bids are found, they are stored in a list and sorting so that the highest bid is at the beginning
                if current_bids:
                    for i in current_bids:
                        abid = i.bid
                        user_bids.append(abid)

                    user_bids.sort(reverse=True)
                    highest_bid = user_bids[0]

                    #Checks if user's bid is less than the current highest bid
                    if bid < highest_bid:
                        return render(request, "auctions/listing.html", {
                        "item" : item,
                        "bid_form" : bid_form,
                        "com_form" : comment_form,
                        "comments" : comments,
                        "in_watchlist" : in_watchlist,
                        "current_bids" : current_bids,
                        "message" : f"Your bid of ${bid:,.2f} is less than the current highest bid of ${highest_bid:,.2f}.",
                        "is_closed" : status,
                        "winner" : thewinner
                    })

                new_bid = Bid(
                    name=user,
                    bid=bid,
                    date=date,
                    item=theitem
                )

                new_bid.save()

                current_bids = Bid.objects.filter(item=item).order_by('-date')

                return render(request, "auctions/listing.html", {
                    "item" : item,
                    "bid_form" : bid_form,
                    "com_form" : comment_form,
                    "comments" : comments,
                    "in_watchlist" : in_watchlist,
                    "current_bids" : current_bids,
                    "message" : "Your bid was placed successfully!",
                    "is_closed" : status,
                    "winner" : thewinner
                })

        if 'thecomment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                commenter = request.user
                comment = comment_form.cleaned_data["thecomment"]
                date = datetime.now().date()
                com_item = item

                new_comment = Comments(
                    name=commenter,
                    comment=comment,
                    thedatetime=date,
                    item=com_item
                )

                new_comment.save()

                return HttpResponseRedirect(reverse("listing", args=[item.id]))

            else:
                return render(request, "auctions/listing.html", {
                    "item" : item,
                    "bid_form" : bid_form,
                    "com_form" : comment_form,
                    "comments" : comments,
                    "in_watchlist" : in_watchlist,
                    "current_bids" : current_bids,
                    "is_closed" : status,
                    "winner" : thewinner
                })

@login_required(login_url="/login")
def watchlist(request):
    if request.method == "GET":
        user = request.user
        watchlist, created = Watchlist.objects.get_or_create(user=user)

        if watchlist == None:
            return render(request, "auctions/watchlist.html")

        user_items = watchlist.items.all()
        user_items = [items.id for items in user_items]

        user_watchlist = []
        for item in user_items:
            list = Listing.objects.get(pk=item)
            user_watchlist.append(list)

        return render(request, "auctions/watchlist.html", {
            "items" : user_watchlist
        })

@login_required(login_url="/login")
def close_listing(request, item):
    if request.method == "POST":

        #Gets listing item
        thelisting = Listing.objects.get(pk=item)

        #Extracts all bids for the associated item and sorts in descending order by bid
        try:
            thebids = Bid.objects.filter(item=thelisting).order_by('-bid')
        except ObjectDoesNotExist:
            thebids = None

        #Extracts first user to get winner
        try:
            thelisting.winner = thebids[0].name
            #Sets winner of listing in model
        except IndexError:
            thelisting.winner = None

        #Sets status of listing to closed
        thelisting.is_closed = True

        thelisting.save()

        #Removes item from all current watchlists
        watchlists = Watchlist.objects.filter(items=thelisting)
        for watch in watchlists:
            if watch.user != thelisting.winner:
                watch.items.remove(thelisting)

        return HttpResponseRedirect(reverse("listing", args=[item]))

@login_required(login_url="/login")
def mylistings(request):
    user = request.user
    item = Listing.objects.filter(seller=user)
    return render(request, "auctions/mylistings.html", {
        "item" : item
    })
