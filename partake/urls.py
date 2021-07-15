from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('branch_operations/', include('branch_operations.urls')),
    path('LoginPage/', user_views.LoginPage, name='LoginPage'),
    path('profile_page/', user_views.profile_page, name='profile_page'),
    path('LogoutPage/', user_views.LogoutPage, name='LogoutPage'),
    path('signup/', user_views.signup, name='signup'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="events/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="events/password_reset_done.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="events/password_reset_complete.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

