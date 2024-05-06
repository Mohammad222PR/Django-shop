from django.urls import path
from dashboard.customer.views import contacts as views


urlpatterns = [
    path("contact/list/", views.CustomerContactsListView.as_view(), name="contact-list"),
    path(
        "contact/detail/<int:pk>/",
        views.CustomerContactsDetailView.as_view(),
        name="contact-detail",
    ),
    path(
        "contact/answer/<int:pk>/",
        views.CustomerAnswerContactView.as_view(),
        name="contact-answer",
    ),
    path(
        "contact/close/<int:pk>/",
        views.CustomerContactClosedView.as_view(),
        name="contact-close",
    ),
]
