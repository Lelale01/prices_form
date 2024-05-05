from functools import wraps
from django.contrib import admin
from django import forms
from .models import Producto, Provincia, Region, ListaProducto, Gasto, ListaGasto, TipoComercio
from django.contrib.auth.models import Group
from django.conf import settings
from import_export.admin import ImportExportModelAdmin
from .resources import ListaGastoResource, GastoInlineResource

class GastoInline(admin.TabularInline):
    model = Gasto
    extra = 1
    resource_class = GastoInlineResource

@admin.register(ListaGasto)
class ListaGastoAdmin(ImportExportModelAdmin):
    resource_class = ListaGastoResource
    inlines = [GastoInline]

@admin.register(Gasto)
class GastoAdmin(ImportExportModelAdmin):
    resource_class = GastoInlineResource


group, created = Group.objects.get_or_create(name='visores')

if created:
    group.save()


@admin.register(ListaProducto)
class ListaProductoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'usuario']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']
    def save_model(self, request, obj, form, change):
        if not obj.nombre:
            obj.nombre = form.cleaned_data.get('tipo_fruta')
        obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user.groups.filter(name='visores'):
            return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user.groups.filter(name='visores'):
            return True
        return False


class SuperuserOnlyAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Region)
class RegionAdmin(SuperuserOnlyAdmin):
    list_display = ['nombre']

@admin.register(Provincia)
class ProvinciaAdmin(SuperuserOnlyAdmin):
    list_display = ['nombre']

@admin.register(TipoComercio)
class TipoComercioAdmin(SuperuserOnlyAdmin):
    list_display = ['tipo']
    exclude = ['listaProducto']
