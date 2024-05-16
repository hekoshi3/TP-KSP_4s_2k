from django.urls import path
from myapp.views import image_generation_view, register_user, login_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sdgen', image_generation_view, name='image_generation'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
