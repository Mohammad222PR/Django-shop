from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView


from dashboard.mixins.dashboard import AdminDashBoardMixin


# Create your views here.


class AdminDashBoardHomeView(AdminDashBoardMixin, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/admin/home.html"
