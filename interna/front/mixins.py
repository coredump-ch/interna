from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    """
    Require login as staff.
    """
    def test_func(self):
        return self.request.user.is_staff