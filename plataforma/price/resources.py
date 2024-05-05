from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import ListaGasto, Gasto

class ListaGastoResource(resources.ModelResource):
    class Meta:
        model = ListaGasto
        fields = ('fecha', 'usuario__username', 'tipoComercio__tipo') 


class GastoInlineResource(resources.ModelResource):
    listaGasto = fields.Field(
        column_name='listaGasto',
        attribute='listaGasto',
        widget=ForeignKeyWidget(ListaGasto, 'nombre')
    )

    class Meta:
        model = Gasto
        fields = ('producto', 'costo', 'listaGasto')