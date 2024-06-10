from typing import Any
from django.views import generic, View
from dashboard.mixins.admin import HasAdminAccessPermission
from group_email.models import GroupEmail, GroupEmailStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from website.models import NewsLetter
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import User
from ..forms.group_email import ChangeGroupEmailDataForm, GroupEmailStartForm
class AdminGroupEmailListView(LoginRequiredMixin, HasAdminAccessPermission, generic.ListView):
    template_name = 'dashboard/admin/group_email/email_list.html'
    queryset = GroupEmail.objects.all()
    paginate_by = 7
    context_object_name = 'group_emails'
    

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)
    

    def get_queryset(self):
        request = self.request
        queryset = GroupEmail.objects.all()
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

    


class AdminGroupEmailStartView(LoginRequiredMixin,SuccessMessageMixin, HasAdminAccessPermission, generic.CreateView):
    template_name = 'dashboard/admin/group_email/email_start.html'
    form_class = GroupEmailStartForm  
    queryset = GroupEmail.objects.all()
    success_message = "با موفقیت ساخته شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.to_email = list(User.objects.values_list('email', flat=True))
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:group-email-update", kwargs={"pk": form.instance.pk}))
    
    def get_success_url(self) -> str:
        return reverse_lazy("dashboard:admin:group-email-list")

class AdminGroupEmailUpdateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin ,generic.UpdateView):
    template_name = 'dashboard/admin/group_email/email_update.html'
    form_class = GroupEmailStartForm
    queryset = GroupEmail.objects.all()
    success_message = "با موفقیت به روز رسانی شد"


    def get_success_url(self):
        return reverse_lazy("dashboard:admin:group-email-update", kwargs = {'pk': self.object.pk})
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['to_email_emails'] = self.object.to_email
        return context