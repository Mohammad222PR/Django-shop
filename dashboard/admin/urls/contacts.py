from django.urls import path
from dashboard.admin.views import contacts as views


urlpatterns = [
    path("contact/list/", views.AdminContactsListView.as_view(), name="contact-list"),
    path(
        "contact/detail/<int:pk>/",
        views.AdminContactsDetailView.as_view(),
        name="contact-detail",
    ),
    path(
        "contact/answer/<int:pk>/",
        views.AdminAnswerContactView.as_view(),
        name="contact-answer",
    ),
    path(
        "contact/close/<int:pk>/",
        views.AdminContactClosedView.as_view(),
        name="contact-close",
    ),
]
