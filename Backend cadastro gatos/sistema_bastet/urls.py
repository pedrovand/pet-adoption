from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from gatos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gatos/', views.listar_gatos),
    path('gestao/', include('gatos.urls')),
    re_path(r'^(?P<filename>(index|animais|como-adotar|contato|quero-ajudar)\.html)$', views.serve_html_page),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static('/src/', document_root=str(settings.BASE_DIR.parent / 'src'))