import json
import decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.views.decorators.csrf import csrf_exempt
from .models import Listing, Bid, Comment, Category, User, Watchlist
from .forms import BidForm, ListingCreateForm, CommentForm, ListingUpdateForm


def categories(request):
    return {"categories": Category.objects.all()}


def watchlist(request):
    if request.user.is_authenticated:
        return {"watchlist": Watchlist.objects.filter(user=request.user)}
    else:
        return {"watchlist": []}


@csrf_exempt
def add_to_watchlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_data = json.loads(request.body.decode("utf-8"))
            listing_id = post_data.get("listing_id")
            listing = Listing.objects.filter(id=listing_id).first()
            user = request.user
            try:
                obj = Watchlist.objects.filter(user=user, listing=listing).first()
                if obj:
                    return JsonResponse({"success": True})
                else:
                    obj = Watchlist(user=user, listing=listing)
                    obj.save()
                    return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": False})


@csrf_exempt
def remove_from_watchlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_data = json.loads(request.body.decode("utf-8"))
            listing_id = post_data.get("listing_id")
            listing = Listing.objects.filter(id=listing_id).first()
            user = request.user
            try:
                obj = Watchlist.objects.filter(user=user, listing=listing).first()
                if obj:
                    obj.delete()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": False})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class Index(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "listings"
    paginate_by = 6

    def get_queryset(self):
        return Listing.objects.all().filter(is_active=True)
        # return Listing.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["bids"] = Bid.objects.all()
        return context


class ListingDetail(DetailView):
    model = Listing
    template_name = "auctions/listing_detail.html"
    context_object_name = "listing"
    form = CommentForm
    bid_form = BidForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bids"] = Bid.objects.filter(listing=self.object)
        context["comments"] = Comment.objects.filter(listing=self.object)
        context["watchlist_true"] = Watchlist.objects.filter(user=self.request.user, listing=self.object)
        context["is_owner"] = self.request.user == self.object.user
        context["form"] = self.form
        context["bid_form"] = self.bid_form
        context["is_active"] = self.object.is_active
        context["highest_bidder"] = Bid.objects.filter(listing=self.object).order_by("-amount").first()
        context["winner"] = self.object.winner
        context["is_winner"] = self.request.user == self.object.winner
        return context


class CreateListing(CreateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = "auctions/create_listing.html"
    form = ListingCreateForm
    extra_context = {"form": form}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("listing_detail", kwargs={"slug": self.object.slug})


def update_listing(request, slug):
    listing = Listing.objects.filter(slug=slug).first()
    if listing.user == request.user:
        if request.method == "POST":
            form = ListingCreateForm(request.POST, instance=listing)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
            else:
                return render(request, "auctions/update_listing.html", {"form": form})
        else:
            form = ListingCreateForm(instance=listing)
            return render(request, "auctions/update_listing.html", {"form": form})


class WatchlistView(ListView):
    model = Listing
    template_name = "auctions/watchlist.html"
    context_object_name = "listing"
    paginate_by = 5

    def get_queryset(self):
        return Listing.objects.all().filter(is_active=True)
        # return Listing.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bids"] = Bid.objects.all()
        return context


def add_a_comment(request, slug):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = Listing.objects.get(slug=slug)
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
    else:
        return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))


class CatagoryListView(ListView):
    model = Listing
    template_name = "auctions/catagory_list.html"
    context_object_name = "listings"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.category = self.kwargs.get("category")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        category = self.request.GET.get("q")
        # return Listing.objects.all().filter(is_active=True, category=self.kwargs["category"])
        return Listing.objects.filter(is_active=True, category=self.kwargs["slug"]).all()
        # return Listing.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = self.request.GET.get("q")
        context["bids"] = Bid.objects.all()
        return context


def place_bid(request, slug):
    if request.method == "POST":
        form = BidForm(request.POST)
        listing = Listing.objects.get(slug=slug)
        if listing.is_active == False:
            messages.error(request, "Sorry Auction Has Already Closed.", extra_tags="alert-danger")
            return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
        if form.is_valid():
            bid_obj = Bid.objects.filter(listing=listing).order_by("-amount").first()
            if not bid_obj:
                starting_bid = listing.starting_bid
                current_bid = decimal.Decimal(0.00) if starting_bid is None else starting_bid
            else:
                current_bid = decimal.Decimal(bid_obj.amount)
            if form.cleaned_data["amount"] > current_bid:
                bid = form.save(commit=False)
                bid.listing = Listing.objects.get(slug=slug)
                bid.user = request.user
                bid.save()
                messages.success(request, "Bid placed successfully.", extra_tags="alert-success")
                return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
            else:
                messages.error(request, "Bid must be higher than current bid.", extra_tags="alert-danger")
                return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
    else:
        return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))


def close_listing(request, slug):
    listing = Listing.objects.get(slug=slug)
    if listing.user == request.user:
        listing.is_active = False
        winner = Bid.objects.filter(listing=listing).order_by("-amount").first()
        listing.winner = winner.user
        listing.save()
        return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
    else:
        return HttpResponseRedirect(reverse("listing_detail", kwargs={"slug": slug}))
