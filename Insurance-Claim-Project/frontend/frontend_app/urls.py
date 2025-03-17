from django.contrib import admin
from django.urls import path
from .views import home, profile, upload_claim, claim_list
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('profile/', profile, name = 'profile'),
    path('upload-claim/', upload_claim, name='upload_claim'),
    path('claims/', claim_list, name='claim_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)