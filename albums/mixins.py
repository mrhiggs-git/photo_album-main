from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AlbumOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only the album owner or a superuser can edit/delete the album."""
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.owner or self.request.user.is_superuser


class PhotoOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only the photo uploader, album owner, or superuser can delete a photo."""
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return (
            user == obj.uploaded_by or
            user == obj.album.owner or
            user.is_superuser
        )


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict a view to staff/admin users only."""
    def test_func(self):
        return self.request.user.is_staff