from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, User, Listing, Bid, Comment, Watchlist

admin.site.register(User, UserAdmin)
admin.site.site_header = "zBay Admin"
admin.site.site_title = "zBay Admin"
admin.site.index_title = "zBay Admin"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "starting_bid",
        "category",
        "is_active",
        "end_date",
        "image_url",
        "slug",
    )
    list_filter = ("category",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title", "category")}


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "amount", "bid_time", "slug")
    list_filter = ("user", "listing")
    search_fields = ("user", "listing")
    prepopulated_fields = {"slug": ("listing", "bid_time", "amount")}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "listing", "created", "updated", "slug")
    list_filter = ("user", "listing")
    search_fields = ("user", "listing")
    prepopulated_fields = {"slug": ("listing", "user", "created")}


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "created", "slug")
    list_filter = ("user", "listing")
    search_fields = ("user", "listing")
    prepopulated_fields = {"slug": ("user", "listing")}


# admin.site.register(Listing)
# admin.site.register(Bid)
# admin.site.register(Comment)
# admin.site.register(Watchlist)
# admin.site.register(Category)
