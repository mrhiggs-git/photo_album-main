from django.contrib import admin
from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['title', 'owner__username']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'album', 'uploaded_by', 'uploaded_at']
    list_filter = ['album']
    search_fields = ['caption', 'album__title']