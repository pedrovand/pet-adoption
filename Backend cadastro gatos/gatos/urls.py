from django.urls import path

from . import views

app_name = 'gatos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('loginbastet/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pets/novo/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/editar/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/excluir/', views.pet_delete, name='pet_delete'),
]