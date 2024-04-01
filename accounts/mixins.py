from django.shortcuts import redirect


class RegisterViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("website:home")
        return super().dispatch(request, *args, **kwargs)
