from cart.cart import CartSession


def cart_processor(request):
    cart = CartSession(request.session)
    total_quantity = cart.get_total_quantity()
    cart_items = cart.get_cart_items()
    return {"cart": cart, "total_quantity": total_quantity, "cart_items": cart_items}