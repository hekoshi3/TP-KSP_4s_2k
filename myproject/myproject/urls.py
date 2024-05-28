from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.redirect_to_profile, name='redirect_to_profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('user_profile/', views.profile, name='user_profile'),
    path('gallery/', views.gallery_view, name='gallery_view'),
    path('sdgen/', views.image_generation_view, name='image_generation'),
    path('', RedirectView.as_view(url='sdgen/', permanent=False), name='index_redirect'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
