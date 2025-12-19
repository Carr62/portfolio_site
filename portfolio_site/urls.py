from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 1. Import the view from your app
from portfolio.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # API endpoints
    path("api/", include("portfolio.urls")),

    # 2. The Homepage Path
    # When the URL is empty (e.g., http://127.0.0.1:8000/), call the 'index' view
    path("", index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)