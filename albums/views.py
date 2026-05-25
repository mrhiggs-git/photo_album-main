from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Album, Photo
from .mixins import AlbumOwnerMixin, PhotoOwnerMixin




class RegisterView(FormView):
    template_name = 'albums/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)




class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(
            Q(owner=user) | Q(is_public=True)
        ).distinct()


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(
            Q(owner=user) | Q(is_public=True)
        ).distinct()


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    template_name = 'albums/album_form.html'
    fields = ['title', 'description', 'is_public']
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(AlbumOwnerMixin, UpdateView):
    model = Album
    template_name = 'albums/album_form.html'
    fields = ['title', 'description', 'is_public']
    success_url = reverse_lazy('album-list')


class AlbumDeleteView(AlbumOwnerMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'albums/photo_form.html'
    fields = ['image', 'caption']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = get_object_or_404(Album, pk=self.kwargs['album_pk'])
        return context

    def form_valid(self, form):
        album = get_object_or_404(
            Album,
            pk=self.kwargs['album_pk'],
            owner=self.request.user
        )
        form.instance.album = album
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.kwargs['album_pk']})


class PhotoDeleteView(PhotoOwnerMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})