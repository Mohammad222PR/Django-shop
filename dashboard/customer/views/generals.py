from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView


from dashboard.mixins.dashboard import CustomerDashBoardMixin


# Create your views here.


class CustomerDashBoardHomeView(CustomerDashBoardMixin, LoginRequiredMixin, TemplateView):
    template_name = "dashboard/customer/home.html"
