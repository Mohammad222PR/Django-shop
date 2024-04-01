"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# ________MAIN URLS________
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls", namespace="website")),  # website app main route
    path(
        "accounts/", include("accounts.urls", namespace="accounts")
    ),  # accounts app main route
    path("shop/", include("shop.urls", namespace="shop")),  # shop app main route
    path("cart/", include("cart.urls", namespace="cart")),  # cart app main route
    # ______CKEDITOR_______#
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# route Debugger toolbar
if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

# loading static and media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
