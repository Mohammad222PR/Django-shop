from typing import Any
from django.views import generic, View
from dashboard.mixins.admin import HasAdminAccessPermission
from group_email.models import GroupEmail, GroupEmailStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from ..forms.group_email import ChangeGroupEmailDataForm

class AdminGroupEmailListView(LoginRequiredMixin, HasAdminAccessPermission, generic.ListView):
    template_name = 'dashboard/admin/group_email/email_list.html'
    queryset = GroupEmail.objects.all().distinct(id)
    paginate_by = 7
    context_object_name = 'group_email'
    

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)
    

    def get_queryset(self):
        request = self.request
        queryset = GroupEmail.objects.all().distinct(id)
        if search_q := request.GET.get("q", None):
            queryset = queryset.filter(subject__icontains=search_q)

        if status := request.GET.get("status", None):
            queryset = queryset.filter(status=status)

        if order_by := request.GET.get("order_by", None):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = GroupEmail.objects.all().count()
        context['user_username'] = GroupEmail.user.user_profile.full_name
        return context

class AdminGroupEmailChangeView(LoginRequiredMixin,  HasAdminAccessPermission, View):

    def post(self, request):
        form = ChangeGroupEmailDataForm(request.POST)

        if not form.is_valid():
            messages.error(request, "فرم معتبر نمی باشد")
            return redirect("dashboard:admin:users-list")

        change_type = request.POST.get("change_type")
        selected_group_email = request.POST.getlist("selected_group_email")

        for group_email_id in selected_group_email:
            group_email = get_object_or_404(GroupEmail, id=group_email_id)

            if change_type in ["published", "draft", "cancelled"]:
                self.change_status(group_email, change_type)


        messages.success(request, "باموفقیت بروز شد")
        return redirect("dashboard:admin:users-list")
    

    def change_status(self, group_email, status):
        if group_email.status != GroupEmailStatus[status].value:
            group_email.status = GroupEmailStatus[status].value
            group_email.save()

    