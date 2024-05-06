from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from cart.models import Cart, CartItem
from shop.models import Product, ProductStatus

CART_SESSION_ID = "cart"


class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault(CART_SESSION_ID, {"items": []})

    def add_product(self, product_id, quantity):
        # product = Product.objects.get(id=product_id)
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if (
                    not item["quantity"] >= 10
                    or not item["quantity"]
                    > self._get_product_by_id(item["product_id"]).stock
                ):
                    item["quantity"] += int(quantity)
                else:
                    return messages.error(
                        self.request,
                        "شما نمیتونید از یک محصول بیش از 10 تا داشته باشید",
                    )
                # product.stock -= int(quantity)
                # product.save()
                break
        else:
            self._cart["items"].append(
                {"product_id": product_id, "quantity": int(quantity)}
            )
            # product.stock -= int(quantity)
            # product.save()

        self.save()

    def remove_product(self, product_id):
        # product = Product.objects.get(id=product_id)

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                # product.stock += int(item["quantity"])
                # product.save()
                break
        else:
            pass
        self.save()

    def update_product_quantity(self, product_id, quantity):
        # product = Product.objects.get(id=product_id)

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                # if int(quantity) > item['quantity']:
                #     product.stock -= int(quantity)
                #     product.save()
                # else:
                #     product.stock += int(quantity)
                #     product.save()
                if not item["quantity"] >= 10 or not item[
                    "quantity"
                ] > self._get_product_by_id(item["product_id"]):
                    item["quantity"] = int(quantity)
                else:
                    return JsonResponse(
                        {
                            "message": "شما نمیتوانید بیش از 10 محصول از هر محصول داشته باشید"
                        }
                    )
                break
        else:
            pass
        self.save()

    def get_cart_dict(self):
        return self._cart

    def get_cart_items(self):
        cart_items = self._cart["items"]
        for item in cart_items:
            product_obj = self._get_product_by_id(item["product_id"])
            item.update(
                {
                    "product_obj": product_obj,
                    "total_price": item["quantity"] * product_obj.get_price(),
                }
            )
        return cart_items

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])

    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def save(self):
        self.session.modified = True

    def _get_product_by_id(self, product_id):
        try:
            return get_object_or_404(
                Product, id=product_id, status=ProductStatus.published.value
            )
        except Product.DoesNotExist:
            return None

    def sync_cart_items_form_db(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {
                    "product_id": str(cart_item.product.id),
                    "quantity": cart_item.quantity,
                }
                self._cart["items"].append(new_item)
            self.merge_session_cart_in_db(user=user)
            self.save()

    def merge_session_cart_in_db(self, user):
        cart, created = Cart.objects.get_or_create(user=user)

        for item in self._cart["items"]:
            product_obj = self._get_product_by_id(item["product_id"])
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product_obj
            )
            cart_item.quantity = item["quantity"]
            cart_item.save()
        session_product_ids = [item["product_id"] for item in self._cart["items"]]
        CartItem.objects.filter(cart=cart).exclude(
            product__id__in=session_product_ids
        ).delete()
