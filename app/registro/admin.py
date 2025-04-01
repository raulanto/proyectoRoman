from django.contrib import admin
from .models import Registro
# Register your models here.

# admin.site.register(Registro)

# Define the admin class
@admin.register(Registro)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('apellido','ciudad')
    list_editable = ('apellido','email','telefono')
    fieldsets = (
        ("Datos Personales", {
            'fields': ('nombre', 'apellido', 'email', 'telefono')
        }),
        ("Situacion fiscal", {
            'fields': ('rfc', 'regimen')
        }),

    )