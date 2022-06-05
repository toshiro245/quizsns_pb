from django.conf.urls import handler500
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include

from . import settings
from quizpost import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('accounts.urls')),
    path('quizpost/', include('quizpost.urls'))
]

handler404 = views.page_not_found
handler500 = views.server_error

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
