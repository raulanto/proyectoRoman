from django.db import models

# Create your models here.
class Registro(models.Model):
    # Datos Personales
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)

    #Datos Situsacion Fiscial
    rfc = models.CharField(max_length=9, null=True, blank=True)
    curp = models.CharField(max_length=100, null=True, blank=True)
    # a que regimen pertenece
    regimen=models.CharField(max_length=100, null=True, blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #Direccion
    colonia = models.CharField(max_length=100, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    pais = models.CharField(max_length=100, null=True, blank=True)

    #estado de la Persona
    estado_civil = models.CharField(max_length=20, null=True, blank=True)
    ocupacion = models.CharField(max_length=100, null=True, blank=True)
    escolaridad = models.CharField(max_length=100, null=True, blank=True)

    #datos de la empresa donde trabaja
    telefono_emergencia = models.CharField(max_length=15, null=True, blank=True)
    parentesco = models.CharField(max_length=50, null=True, blank=True)
    nombre_emergencia = models.CharField(max_length=100, null=True, blank=True)
    apellido_emergencia = models.CharField(max_length=100, null=True, blank=True)
    nombre_referencia = models.CharField(max_length=100, null=True, blank=True)
    apellido_referencia = models.CharField(max_length=100, null=True, blank=True)
    telefono_referencia = models.CharField(max_length=15, null=True, blank=True)

    # Contancto de persona
    nombre_empresa = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    antiguedad = models.IntegerField(null=True, blank=True)
    sueldo_empresa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    telefono_empresa = models.CharField(max_length=15, null=True, blank=True)
    direccion_empresa = models.CharField(max_length=100, null=True, blank=True)
    cp_empresa = models.CharField(max_length=10, null=True, blank=True)

    mascotas=models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"