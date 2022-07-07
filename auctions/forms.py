from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms.models import fields_for_model
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Listing, Bid, Comment

User = get_user_model()


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {"username": {"unique": _("This username has already been taken.")}}


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "category", "image_url"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "description": forms.Textarea(attrs={"class": "form-control mb-3"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control mb-3"}),
            "category": forms.Select(attrs={"class": "form-control mb-3"}),
            "image_url": forms.TextInput(attrs={"class": "form-control mb-3"}),
        }


class ListingUpdateForm(forms.Form):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "category", "image_url"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "description": forms.Textarea(attrs={"class": "form-control mb-3"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control mb-3"}),
            "category": forms.Select(attrs={"class": "form-control mb-3"}),
            "image_url": forms.TextInput(attrs={"class": "form-control mb-3"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Make A Comment"}
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control mb-3"}),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {"amount": "Bid Amount"}
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control mb-3"}),
        }
