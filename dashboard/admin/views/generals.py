from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView


from dashboard.mixins.admin import HasAdminAccessPermission


# Create your views here.


class AdminDashBoardHomeView(HasAdminAccessPermission, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/admin/home.html"
