from django import template
from ..models import Watchlist


register = template.Library()


@register.simple_tag(takes_context=True)
def add_item(context):
    """
    Adds the item to the watchlist.
    """
    user = context["request"].user
    listing = context["listing"]
    if not Watchlist.objects.filter(user=user, listing=listing).exists():
        Watchlist.objects.create(user=user, listing=listing)
        return True
    return False
