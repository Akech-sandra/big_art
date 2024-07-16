from django import template

register = template.Library()

@register.filter
def get_product_quantity(cart, product_id):
    return cart.get(str(product_id), 0)

@register.filter
def remaining_quantity(product, cart):
    cart_quantity = cart.get(str(product.id), 0)
    return product.remaining_quantity - cart_quantity

