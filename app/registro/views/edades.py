from django.views import View
from django.shortcuts import render
from registro.models import Registro
from django.db.models import Count, Avg, Max, Min, StdDev
from django.db.models import Case, When, Value, CharField
import json
import numpy as np
from datetime import datetime


class Edades(View):
    """
    Vista para mostrar estadísticas y gráficos relacionados con las edades de los registros
    """

    def get(self, request, *args, **kwargs):
        # Estadísticas básicas de edad
        age_stats = Registro.objects.aggregate(
            avg_age=Avg('edad'),
            max_age=Max('edad'),
            min_age=Min('edad'),
            std_dev=StdDev('edad'),
            count=Count('id')
        )

        # Convertir Decimal a float para serialización JSON
        age_stats = {k: float(v) if v is not None else 0 for k, v in age_stats.items()}

        # Distribución por grupos de edad
        age_groups = (
            Registro.objects
            .annotate(
                age_group=Case(
                    When(edad__lt=18, then=Value('Menor de 18')),
                    When(edad__gte=18, edad__lt=25, then=Value('18-24')),
                    When(edad__gte=25, edad__lt=35, then=Value('25-34')),
                    When(edad__gte=35, edad__lt=45, then=Value('35-44')),
                    When(edad__gte=45, edad__lt=55, then=Value('45-54')),
                    When(edad__gte=55, edad__lt=65, then=Value('55-64')),
                    When(edad__gte=65, then=Value('65+')),
                    output_field=CharField(),
                )
            )
            .values('age_group')
            .annotate(count=Count('id'))
            .order_by('age_group')
        )

        # Histograma de edades
        ages = list(Registro.objects.values_list('edad', flat=True))
        bins = np.arange(0, 110, 10)  # Rangos de 10 años desde 0 a 100+
        hist, bin_edges = np.histogram(ages, bins=bins)

        # Convertir arrays de NumPy a listas de Python
        age_histogram = {
            'labels': [f"{int(bin_edges[i])}-{int(bin_edges[i + 1]) - 1}" for i in range(len(bin_edges) - 1)],
            'data': hist.tolist()  # Convertir array de NumPy a lista
        }

        # Boxplot statistics - convertir todos los valores a float
        boxplot_stats = {
            'min': float(np.min(ages)),
            'q1': float(np.percentile(ages, 25)),
            'median': float(np.median(ages)),
            'q3': float(np.percentile(ages, 75)),
            'max': float(np.max(ages)),
        }

        # Edad promedio por estado físico - convertir Decimal a float
        avg_age_by_physical = list(
            Registro.objects
            .values('estado_fisico')
            .annotate(avg_age=Avg('edad'), count=Count('id'))
            .order_by('-avg_age')
        )
        for item in avg_age_by_physical:
            item['avg_age'] = float(item['avg_age'])

        # Edad promedio por estado civil - convertir Decimal a float
        avg_age_by_marital = list(
            Registro.objects
            .values('estado_civil')
            .annotate(avg_age=Avg('edad'), count=Count('id'))
            .order_by('-avg_age')
        )
        for item in avg_age_by_marital:
            item['avg_age'] = float(item['avg_age'])

        boxplot_apex_data = {
            'x': 'Distribución de Edades',
            'y': [
                float(boxplot_stats['min']),
                float(boxplot_stats['q1']),
                float(boxplot_stats['median']),
                float(boxplot_stats['q3']),
                float(boxplot_stats['max'])
            ]
        }

        # Preparar datos para gráficos
        context = {
            # Estadísticas básicas
            'age_stats': age_stats,

            # Datos para gráfico de grupos de edad
            'age_groups_labels': json.dumps([g['age_group'] for g in age_groups]),
            'age_groups_data': json.dumps([g['count'] for g in age_groups]),

            # Datos para histograma
            'age_histogram_labels': json.dumps(age_histogram['labels']),
            'age_histogram_data': json.dumps(age_histogram['data']),

            # Datos para boxplot
            'boxplot_stats': json.dumps(boxplot_stats),

            # Datos para gráficos de edad promedio
            'avg_age_physical_labels': json.dumps([x['estado_fisico'].capitalize() for x in avg_age_by_physical]),
            'avg_age_physical_data': json.dumps([x['avg_age'] for x in avg_age_by_physical]),
            'avg_age_marital_labels': json.dumps([x['estado_civil'].capitalize() for x in avg_age_by_marital]),
            'avg_age_marital_data': json.dumps([x['avg_age'] for x in avg_age_by_marital]),

            # Datos para tablas
            'age_groups_table': age_groups,
            'avg_age_physical_table': avg_age_by_physical,
            'avg_age_marital_table': avg_age_by_marital,
            'boxplot_apex_data': json.dumps([boxplot_apex_data]),
        }

        return render(request, 'edades.html', context)