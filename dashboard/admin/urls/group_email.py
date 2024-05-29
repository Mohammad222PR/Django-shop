from django.urls import path
from dashboard.admin.views import group_email as views


urlpatterns = [
    path("group_email/list/", views.AdminGroupEmailListView.as_view(), name="group-email-list"),
    path("group_email/change/", views.AdminGroupEmailChangeView.as_view(), name="group-email-change"),

    # path("detail/<int:pk>/", views.AdminGroupEmailDetailView.as_view(), name="group-email-detail"),
    # path("start/", views.AdminGroupEmailStartView.as_view(), name="group-email-start"),
]
