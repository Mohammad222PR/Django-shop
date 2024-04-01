from django.shortcuts import get_object_or_404

from shop.models import Product, ProductStatus

CART_SESSION_ID = "cart"


class CartSession:
    def __init__(self, session):
        self.session = session
        self.cart = self.session.setdefault(CART_SESSION_ID, {"items": []})

    def add_product(self, product_id, quantity):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += int(quantity)
                break
        else:
            self.cart["items"].append(
                {"product_id": product_id, "quantity": int(quantity)}
            )

        self.save()

    def remove_product(self, product_id):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                self.cart["items"].remove(item)
                break
        else:
            pass
        self.save()

    def update_product_quantity(self, product_id, quantity):
        for item in self.cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            pass
        self.save()

    def get_cart_dict(self):
        return self.cart

    def get_cart_items(self):
        cart_items = self.cart["items"]
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
        return sum(item["total_price"] for item in self.cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self.cart["items"])

    def clear(self):
        self.cart = {"items": []}
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
