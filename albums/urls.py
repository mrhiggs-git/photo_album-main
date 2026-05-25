from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('album/create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('album/<int:album_pk>/upload/', views.PhotoUploadView.as_view(), name='photo-upload'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
]