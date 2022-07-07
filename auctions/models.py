from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    # Watchlist


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse("catagory_detail", args=[self.slug])

    def __str__(self):
        return self.name


# class ListingManager(models.Manager):
#     def active(self):
#         return super().get_queryset().filter(is_active=True)

#     def expired(self):
#         return super().get_queryset().filter(is_active=False)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True, max_length=500, null=True)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    # history = models.ManyToManyField(User, through="Bid", related_name="bids")
    image_url = models.URLField(blank=True, null=True, default="https://via.placeholder.com/150")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winner")
    # objects = models.Manager()
    # ListingManager = ListingManager()

    class Meta:
        verbose_name_plural = "Listings"
        ordering = ("-starting_bid",)

    def add_to_watchlist(self, user, Watchlist):
        try:
            obj = Watchlist.objects.get(user=user, listing=self)
            if obj:
                return False
            else:
                obj = Watchlist(user=user, listing=self)
                obj.save()
                return True
        except:
            return False

    def get_current_bid(self):
        try:
            return Bid.objects.all().filter(listing=self).order_by("-amount")[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        return reverse("listing_detail", args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.start_date}")
        if not self.start_date:
            self.start_date = timezone.now()
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=7)
        super().save(*args, **kwargs)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "Bids"
        ordering = (
            "-listing",
            "-amount",
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user} bid ${self.amount}")
        if not self.bid_time:
            self.bid_time = timezone.now()
            super().save(*args, **kwargs)

    def place_bid(self, bid_amount):
        if bid_amount > self.listing.current_bid:
            self.amount = bid_amount
            self.save()
            self.listing.current_bid = bid_amount
            self.listing.save()
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse("bid_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} bid ${self.amount}"


class Comment(models.Model):
    text = models.CharField(max_length=500, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True, blank=True)
    slug = models.CharField(max_length=50)

    class Meta:
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user}-{self.listing}-{self.created}")
            self.user = self.user
            self.listing = self.listing
            self.created = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("comment_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} commented on {self.listing}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="watchlist",
    )
    created = models.DateTimeField()
    slug = models.SlugField(max_length=50)

    class Meta:
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user}-{self.listing}")
            self.created = timezone.now()
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("listing_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} added {self.listing} to watchlist"
