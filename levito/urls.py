"""levito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add   a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views.views_ad import CategoryViewSet, SelectionViewSet
from ads.views.views_us import LocationViewSet

from ads.views.views import index
from levito import settings

router = routers.SimpleRouter()
router.register('location', LocationViewSet)
router_cat = routers.SimpleRouter()
router_cat.register('category', CategoryViewSet)
router_sel = routers.SimpleRouter()
router_sel.register('selection', SelectionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path("cat/", include('ads.urls.urls_cat')),
    path("ad/", include('ads.urls.urls_ad')),
    path("user/", include('ads.urls.urls_us')),
]

urlpatterns += router.urls
urlpatterns += router_cat.urls
urlpatterns += router_sel.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
