from django.urls import path

from . import views
from .views import Index, ListingDetail, CreateListing, WatchlistView, CatagoryListView

urlpatterns = [
    # path("", views.index, name="index"),
    path("", Index.as_view(), name="index"),
    path("listing_detail/<slug:slug>/", ListingDetail.as_view(), name="listing_detail"),
    path("update_listing/<slug:slug>/", views.update_listing, name="update_listing"),
    path("create_listing/", CreateListing.as_view(), name="create_listing"),
    path("close_listing/<slug:slug>/", views.close_listing, name="close_listing"),
    path("place_bid/<slug:slug>/", views.place_bid, name="place_bid"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("catagory/<slug:slug>/", CatagoryListView.as_view(), name="catagory_view"),
    path("add_to_watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path("add_a_comment/<slug:slug>/", views.add_a_comment, name="add_a_comment"),
]
