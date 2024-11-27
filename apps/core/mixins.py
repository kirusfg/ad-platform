from django.contrib.auth.mixins import LoginRequiredMixin


class CoreMixin(LoginRequiredMixin):
    """Base mixin for views requiring authentication"""

    pass
