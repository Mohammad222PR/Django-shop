from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dashboard.customer.forms import UserAddressForm
from dashboard.mixins import HasCustomerAccessPermission
from order.models import UserAddress


class CustomerAddressListView(HasCustomerAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/customer/addresses/address-list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_addresses'] = self.get_queryset().count()
        return context


class CustomerAddressCreateView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "dashboard/customer/addresses/address-create.html"
    form_class = UserAddressForm
    success_message = "ادرس شما با موفقیت اضافه شد"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).distinct()

    def form_valid(self, form):
        if not self.get_queryset().count() >= 3:
            form.instance.user = self.request.user
            super().form_valid(form)
            next_page = self.request.POST.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(reverse_lazy("dashboard:customer:address-update", kwargs={"pk": form.instance.pk}))
        else:
            messages.error(self.request, "شما بیش از سه ادرس دارید حد مجاز ادرس 3 تا است")
            return redirect(reverse_lazy("dashboard:customer:address-list"))

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")


class CustomerAddressUpdateView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "dashboard/customer/addresses/address-update.html"
    form_class = UserAddressForm
    success_message = "ادرس شما با موفقیت بروزرسانی شد"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).distinct()

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-update", kwargs={'pk': self.get_object().pk})


class CustomerAddressDeleteView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = "dashboard/customer/addresses/address-delete.html"
    success_message = "حذف ادرس با موفقیت انجام شد"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")
