from django import template
from core.models import Order,Review

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
@register.simple_tag
def rating_count():
    cmnt = Review.objects.filter().values_list('rate', flat=True).order_by('id')
    count = 0
    for cmn in cmnt:
            count+=cmn
    co = int(cmnt.count())
    rat = count/co
    return rat
    