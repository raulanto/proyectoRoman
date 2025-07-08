from django.views import View
from django.shortcuts import render
from registro.models import Registro
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count
import json
from datetime import datetime
from django.utils import timezone
from datetime import datetime, timedelta

class Index(View):
    """
    Dashboard view for Registro model.
    Shows a table of registros and charts with statistics.
    """

    def get(self, request, *args, **kwargs):
        # Get all registros for the table
        registros = Registro.objects.all()
        total_mujeres = registros.filter(sexo='mujer').count()
        total_hombres = registros.filter(sexo='hombre').count()
        # Prepare data for registration by month/year chart
        registrations_by_month_year = (
            Registro.objects
            .annotate(
                year=ExtractYear('fecha_registro'),
                month=ExtractMonth('fecha_registro')
            )
            .values('year', 'month')
            .annotate(count=Count('id'))
            .order_by('year', 'month')
        )

        # Prepare labels and data for the area chart
        labels = []
        data = []
        for entry in registrations_by_month_year:
            year = entry['year']
            month = entry['month']
            month_name = datetime(year, month, 1).strftime('%B %Y')  # Formato "Enero 2023"
            labels.append(month_name)
            data.append(entry['count'])

        # Prepare data for users by estado fisico chart
        users_by_estado_fisico = (
            Registro.objects
            .values('estado_fisico')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        estado_fisico_labels = [entry['estado_fisico'].capitalize() for entry in users_by_estado_fisico]
        estado_fisico_data = [entry['count'] for entry in users_by_estado_fisico]
        total_registros = registros.count()
        registros_vivos = registros.filter(estado_fisico='vivo').count()
        registros_muertos = registros.filter(estado_fisico='muerto').count()

        # Obtener el mes actual y el anterior
        today = datetime.now()
        current_month = today.replace(day=1)
        previous_month = (current_month - timedelta(days=1)).replace(day=1)

        # Contar registros del mes actual
        current_month_count = Registro.objects.filter(
            fecha_registro__month=current_month.month,
            fecha_registro__year=current_month.year
        ).count()

        # Contar registros del mes anterior
        previous_month_count = Registro.objects.filter(
            fecha_registro__month=previous_month.month,
            fecha_registro__year=previous_month.year
        ).count()

        # Calcular porcentaje de cambio
        if previous_month_count > 0:
            percent_change = ((current_month_count - previous_month_count) / previous_month_count) * 100
        else:
            percent_change = 100 if current_month_count > 0 else 0
        context = {
            'registros': registros,
            'registrations_labels': json.dumps(labels),
            'registrations_data': json.dumps(data),
            'estado_fisico_labels': json.dumps(estado_fisico_labels),
            'estado_fisico_data': json.dumps(estado_fisico_data),
            'total_registros': total_registros,
            'registros_vivos': registros_vivos,
            'registros_muertos': registros_muertos,
            'current_month_count': current_month_count,
            'percent_change': percent_change,
            'is_increase': percent_change >= 0,
            'total_mujeres': total_mujeres,
            'total_hombres': total_hombres,
        }

        return render(request, 'home.html', context)
