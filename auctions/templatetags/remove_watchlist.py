from django import template
from ..models import Watchlist


register = template.Library()


@register.simple_tag
def remove_item(listing, user):
    """
    Remove the item to the watchlist.
    """
    try:
        Watchlist.objects.get(user=user, listing=listing).delete()
        return True
    except:
        return False
