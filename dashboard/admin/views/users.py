from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from dashboard.mixins.admin import HasAdminAccessPermission
from ..forms.reviews import ReviewForm
from dashboard.admin.mixins.reviews import ReviewUpdateFormMixin
from accounts.models import User, UserType
from ..forms.users import UserForm, ChangeUserDataForm
from django.db.models import F, Q
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

class AdminUsersListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/users/users-list.html"
    paginate_by = 7
    context_object_name = "users"

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = (
            User.objects.filter(is_superuser=False, type=UserType.customer.value)
            .distinct()
            .order_by("-created_date")
        )
        request = self.request

        if search_q := request.GET.get("q", None):
            queryset = queryset.filter(Q(email__icontains=search_q))

        if order_by := request.GET.get("order_by", None):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_user"] = self.get_queryset().count()
        return context


class AdminUsersDeleteView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView
):
    template_name = "dashboard/admin/users/users-delete.html"
    success_message = "کاربر مورد نظر با موفقیت حذف شد"
    success_url = reverse_lazy("dashboard:admin:users-list")

    def get_queryset(self):
        return (
            User.objects.filter(is_superuser=False, type=UserType.customer.value)
            .distinct()
            .order_by("-created_date")
        )


class AdminUsersUpdateView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/users/users-update.html"
    success_message = "کاربر مورد نظر با موفقیت ویرایش شد"
    form_class = UserForm

    def get_queryset(self):
        return (
            User.objects.filter(is_superuser=False, type=UserType.customer.value)
            .distinct()
            .order_by("-created_date")
        )

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:users-update", kwargs={"pk": self.kwargs.get("pk")}
        )




class AdminChangeUserDataVeiw(LoginRequiredMixin,  HasAdminAccessPermission, View):

    def post(self, request):
        form = ChangeUserDataForm(request.POST)

        if not form.is_valid():
            messages.error(request, "فرم معتبر نمی باشد")
            return redirect("dashboard:admin:users-list")

        change_type = request.POST.get("change_type")
        selected_user = request.POST.getlist("selected_user")

        for user_id in selected_user:
            user = get_object_or_404(User, id=user_id)

            if change_type == 'disable':
                self.change_to_disable(user)

            if change_type == 'enable':
                self.change_to_enable(user)

        messages.success(request, "باموفقیت بروز شد")
        return redirect("dashboard:admin:users-list")
    

    def change_to_disable(self, user):
        if user.is_active == True:
            user.is_active = False
            user.save()

    def change_to_enable(self, user):
        if user.is_active == False:
            user.is_active = True
            user.save()
