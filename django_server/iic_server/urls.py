from django.urls import path
from .views import ImageUploadView
from .view_display import index

urlpatterns = [
    path('api/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('', index, name="index")
]