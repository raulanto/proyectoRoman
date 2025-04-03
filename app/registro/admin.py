from django.contrib import admin
from .models import Registro, Pais, Estado, Ciudad


# Register your models here.

# admin.site.register(Registro)

# Define the admin class
@admin.register(Registro)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('apellido', 'ciudad', 'estado_fisico')
    list_editable = ('apellido', 'email', 'telefono')
    fieldsets = (
        ("Datos Personales", {
            'fields': (
            'nombre', 'apellido', 'email', 'telefono', 'curp', 'fecha_nacimiento', 'edad', 'sexo', 'estado_fisico')
        }),
        ("Situacion fiscal", {
            'fields': ('rfc', 'regimen')
        }),
        ("Direccion", {
            'fields': ('colonia', 'calle', 'numero', 'cp', 'ciudad')
        }),
        ("Estado Civil", {
            'fields': ('estado_civil', 'ocupacion', 'escolaridad')
        }),
        ("Datos de la empresa", {
            'fields': ('nombre_empresa', 'puesto', 'fecha_ingreso', 'antiguedad', 'sueldo_empresa', 'telefono_empresa',
                       'direccion_empresa', 'cp_empresa')
        }),
        ("Contacto de persona", {
            'fields': ('nombre_emergencia', 'apellido_emergencia', 'nombre_referencia', 'apellido_referencia',
                       'telefono_referencia', 'telefono_emergencia', 'parentesco')
        }),
        ('Archivos',{
            'fields': ('contrato',)
        })
    )


admin.site.register(Estado)
admin.site.register(Ciudad)
admin.site.register(Pais)
