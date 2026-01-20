from django import template

register = template.Library()

@register.filter
def get_refund(refunds, purchased_property):
    for refund in refunds:
        if refund.purchased_property.id == purchased_property.id:
            return refund
    return None
