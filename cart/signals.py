from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .cart import CartSession


@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    cart = CartSession(request.session)
    cart.sync_cart_items_form_db(user)


@receiver(user_logged_out)
def pre_logout(sender, request, user, **kwargs):
    cart = CartSession(request.session)
    cart.merge_session_cart_in_db(user)
