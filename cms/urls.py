from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import pwa_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('offline/', TemplateView.as_view(template_name='pwa/offline.html'), name='offline'),
    # PWA service worker at root scope
    path('service-worker.js', TemplateView.as_view(template_name='pwa/service-worker.js', content_type='application/javascript')),
    # Generated PNG icons for Android/iOS
    re_path(r'^pwa/icons/icon-(?P<size>192|512)\.png$', pwa_views.pwa_icon, name='pwa_icon'),
    re_path(r'^pwa/icons/icon-(?P<size>192|512)-maskable\.png$', pwa_views.pwa_icon, name='pwa_icon_maskable'),
    path('', include('attendance.urls')),
]
