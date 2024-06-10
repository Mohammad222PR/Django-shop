from django.urls import path
from dashboard.admin.views import group_email as views


urlpatterns = [
    path("group_email/list/", views.AdminGroupEmailListView.as_view(), name="group-email-list"),
    path("group_email/change/", views.AdminGroupEmailChangeView.as_view(), name="group-email-change"),
    path("group_email/start/", views.AdminGroupEmailStartView.as_view(), name="group-email-start"),
    path("group_email/update/<int:pk>/", views.AdminGroupEmailUpdateView.as_view(), name="group-email-update"),

]
