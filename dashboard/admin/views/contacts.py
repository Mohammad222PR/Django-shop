from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
    CreateView,
)
from dashboard.mixins.admin import HasAdminAccessPermission
from ..forms.reviews import ReviewForm
from dashboard.admin.mixins.reviews import ReviewUpdateFormMixin
from accounts.models import User, UserType
from ..forms.users import UserForm
from django.db.models import F, Q
from website.models import ContactUs, AnswerContacts, Status
from ..forms.contacts import AnswerContactForm
from django.shortcuts import redirect
from ..mixins.contacts import ContaxtMixin
from django.views import View


class AdminContactsListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/contacts/contacts-list.html"
    paginate_by = 7
    context_object_name = "contacts"

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = ContactUs.objects.all().distinct()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(
                Q(title__icontains=search_q)
                | Q(first_name__icontains=search_q)
                | Q(last_name__icontains=search_q)
                | Q(phone_number__icontains=search_q)
                | Q(email__icontains=search_q)
            )
        if order_by := self.request.GET.get("order_by", None):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_contacts"] = self.get_queryset().count()
        return context


class AdminContactsDetailView(LoginRequiredMixin, HasAdminAccessPermission, DetailView):
    template_name = "dashboard/admin/contacts/contacts-detail.html"

    def get_queryset(self):
        return ContactUs.objects.all()

    def get_object(self):
        contacts_obj = ContactUs.objects.get(id=self.kwargs.get("pk", None))
        if contacts_obj.status == Status.pending.value:
            contacts_obj.status = Status.seen.value
            contacts_obj.save()
        else:
            pass
        return contacts_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_form"] = AnswerContactForm()
        return context


class AdminAnswerContactView(
    LoginRequiredMixin, ContaxtMixin, HasAdminAccessPermission, CreateView
):
    form_class = AnswerContactForm

    def get_queryset(self):
        return AnswerContacts.objects.all()

    def form_valid(self, form):
        contact_obj = ContactUs.objects.get(id=self.kwargs.get("pk"))
        if contact_obj.status != Status.closed.value:
            form.instance.contact = contact_obj
            form.instance.user = self.request.user
            form.save()
        else:
            messages.error(self.request, "این تیکت قبلا بسته شده است")
            return redirect(
                "dashboard:admin:contact-detail",
                kwargs={"pk": contact_obj.id},
            )

        if contact_obj.status != Status.answerd.value:
            contact_obj.status = Status.answerd.value
            contact_obj.save()
        messages.success(self.request, "پاسخ شما با موفقیت ثبت شد")
        return redirect(
            reverse_lazy(
                "dashboard:admin:contact-detail", kwargs={"pk": self.kwargs.get("pk")}
            )
        )

    def form_invalid(self, form):
        messages.error(self.request, "پاسخ ارسال نشد لطفا مجدد امتحان نمایید")
        return redirect(self.request.META.get("HTTP_REFERER"))


class AdminContactClosedView(LoginRequiredMixin, HasAdminAccessPermission, View):

    def post(self, request, *args, **kwargs):
        contacts_obj = ContactUs.objects.get(id=self.kwargs.get("pk", None))
        if contacts_obj.status != Status.closed.value:
            if contacts_obj.user == request.user or request.user.type in [
                UserType.admin.value,
                UserType.superuser.value,
            ]:
                contacts_obj.status = Status.closed.value
                messages.success(request, "تیکت با موفقیت بسته شد")
                contacts_obj.save()

                return redirect(
                    "dashboard:admin:contact-detail",
                    pk=contacts_obj.pk,
                )
            else:
                messages.error(request, "شما دسترسی برای بستن این تیکت ندارید")
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "این تیکت قبلا بسته شده است")
            return redirect(
                "dashboard:admin:contact-detail",
                kwargs={"pk": contacts_obj.id},
            )
