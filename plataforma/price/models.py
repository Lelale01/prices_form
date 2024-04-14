from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ListaProducto(models.Model):
    fecha = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.fecha)


class TipoComercio(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo


class ListaGasto(models.Model):
    fecha = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tipoComercio = models.ForeignKey(TipoComercio, on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.fecha)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    producto = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    listaGasto = models.ForeignKey(ListaGasto, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.producto

