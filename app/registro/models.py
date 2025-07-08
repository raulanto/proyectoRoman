from django.db import models
from django.contrib.auth.models import User
SEXO = [
    ('mujer', 'Mujer')
    , ('hombre', 'Hombre')]

ESTADO_CIVIL = [
    ('soltero', 'Soltero'),
    ('casado', 'Casado'),
    ('divorciado', 'Divorciado'),
    ('viudo', 'Viudo'),
    ('union libre', 'Union Libre')
]

REGIMEN = [
    ('sueldos_salarios', 'Sueldos y Salarios'),
    ('honorarios', 'Honorarios'),
    ('arrendamiento', 'Arrendamiento'),
    ('actividades_empresariales', 'Actividades Empresariales'),
    ('rif', 'RIF'),
    ('incorporacion_fiscal', 'Incorporación Fiscal')
]

SANGRE=[
    ("a+", "A+"),
    ("a-", "A-"),
    ("b+", "B+"),
    ("b-", "B-"),
    ("ab+", "AB+"),
    ("ab-", "AB-"),
    ("o+", "O+"),
    ("o-", "O-"),
]


class Pais(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural="País"


    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='estados')



    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='ciudades')

    class Meta:
        verbose_name_plural="Ciudades"


    def __str__(self):
        return self.nombre

class Alergia(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.nombre

class Enfermedade(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre



class Registro(models.Model):
    # Datos Personales
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono_celular = models.CharField(max_length=15, null=True, blank=True)
    telefono_casa = models.CharField(max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO, default='mujer')
    estado_fisico = models.CharField(max_length=10, choices=[('vivo', 'Vivo'), ('muerto', 'Muerto')], default='vivo')

    # expediente medico
    tipo_sangre = models.CharField(max_length=10, choices=SANGRE, default='')
    alergias = models.ManyToManyField(Alergia)
    alergias_descrp=models.TextField("Comentario de la Alergia",null=True, blank=True)
    enfermedad = models.ManyToManyField(Enfermedade)
    enfermedad_descrp=models.TextField(
        "Comentario de la enfermedad",
        null=True,
        blank=True,

    )

    # Datos Situsacion Fiscial
    rfc = models.CharField(max_length=9, null=True, blank=True)
    curp = models.CharField(max_length=100, null=True, blank=True)
    # a que regimen pertenece
    regimen = models.CharField(max_length=100,choices=REGIMEN, null=True, blank=True)

    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    # Direccion
    colonia = models.CharField(max_length=100, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    # estado de la Persona
    estado_civil =models.CharField(max_length=11, choices=ESTADO_CIVIL, default='mujer')
    ocupacion = models.CharField(max_length=100, null=True, blank=True)
    escolaridad = models.CharField(max_length=100, null=True, blank=True)

    # Contancto de persona
    telefono_emergencia = models.CharField(max_length=15, null=True, blank=True)
    parentesco = models.CharField(max_length=50, null=True, blank=True)
    nombre_emergencia = models.CharField(max_length=100, null=True, blank=True)
    apellido_emergencia = models.CharField(max_length=100, null=True, blank=True)
    nombre_referencia = models.CharField(max_length=100, null=True, blank=True)
    apellido_referencia = models.CharField(max_length=100, null=True, blank=True)
    telefono_referencia = models.CharField(max_length=15, null=True, blank=True)




    # Datos de la empresa
    nombre_empresa = models.CharField(max_length=100, null=True, blank=True)
    puesto = models.CharField(max_length=100, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    antiguedad = models.IntegerField(null=True, blank=True)
    sueldo_empresa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    telefono_empresa = models.CharField(max_length=15, null=True, blank=True)
    direccion_empresa = models.CharField(max_length=100, null=True, blank=True)
    cp_empresa = models.CharField(max_length=10, null=True, blank=True)

    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)

    usuario_registro =models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='usuario_registro')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


