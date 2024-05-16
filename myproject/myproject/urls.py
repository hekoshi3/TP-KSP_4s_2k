from django.urls import path
from myapp.views import image_generation_view
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('sdgen', image_generation_view, name='image_generation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
