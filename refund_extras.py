from django import template
from app.models import RefundRequest

register = template.Library()

@register.filter
def get_refund(refunds, purchase):
    try:
        return refunds.get(purchased_property=purchase)
    except RefundRequest.DoesNotExist:
        return None
