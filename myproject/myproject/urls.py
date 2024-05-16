from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='user_profile'),
    path('sdgen/', views.image_generation_view, name='image_generation'),
    path('', RedirectView.as_view(url='sdgen/', permanent=False), name='index_redirect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
