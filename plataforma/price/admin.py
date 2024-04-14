from functools import wraps
from django.contrib import admin
from django import forms
from .models import Producto, Provincia, Region, ListaProducto, Gasto, ListaGasto, TipoComercio
from django.contrib.auth.models import Group
from django.conf import settings


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

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    pass

class GastoInline(admin.TabularInline):
    model=Gasto

    categorias = {
        "HARINAS_PANIFICADOS": settings.HARINAS_PANIFICADOS,
        "CEREALES_LEGUMBRES": settings.CEREALES_LEGUMBRES,
        "CARNES": settings.CARNES,
        "OLEOS": settings.OLEOS,
        "LACTEOS": settings.LACTEOS,
        "FRUTAS": settings.FRUTAS,
        "VERDURAS_HORTALIZAS": settings.VERDURAS_HORTALIZAS,
        "DULCES": settings.DULCES,
        "CONDIMENTOS": settings.CONDIMENTOS,
        "BEBIDAS": settings.BEBIDAS,
        "INFUCIONES": settings.INFUCIONES,
    }
    """
    fieldsets = []
    for cat in categorias:
        fieldsets.append((cat, {'fields': (f'producto_{cat}', f'costo_{cat}')}))

    def get_form(self, request, obj=None, **kwargs):
        for cat in self.categorias:
            self.form.base_fields[f'producto_{cat}'].widget.choices = self.categorias[cat]
        return super().get_form(request, obj, **kwargs)
    """


@admin.register(ListaGasto)
class ListaGastoAdmin(admin.ModelAdmin):
    list_display = ["fecha", "tipoComercio"]
    inlines = [GastoInline]
    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        else:
            return ('usuario',)
    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        super().save_model(request, obj, form, change)