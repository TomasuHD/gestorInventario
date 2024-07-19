from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('panel/', Dashboard.as_view(), name='panel'),
    path('agregar/', AddItem.as_view(), name='agregar'),
    path('editar-item/<int:pk>', EditItem.as_view(), name='editar-item'),
    path('eliminar-item/<int:pk>', DeleteItem.as_view(), name='eliminar-item'),
    path('registro/', SignUpView.as_view(), name='registro'),
    path('ingresar/', auth_views.LoginView.as_view(template_name='merma/ingresar.html'), name='ingresar'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(template_name='merma/cerrar-sesion.html'), name="cerrar-sesion"),
    path('reporte/', views.GenerarReporte, name='reporte'),
]