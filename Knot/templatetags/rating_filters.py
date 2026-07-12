from django import template

register = template.Library()


@register.filter
def star_rating(value):
    try:
        rating = int(value)
    except (TypeError, ValueError):
        rating = 0
    stars = '★' * max(0, min(rating, 5))
    return stars
