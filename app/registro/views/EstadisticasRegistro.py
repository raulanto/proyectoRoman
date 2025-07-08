# views.py
from django.views import View
from django.shortcuts import render
from django.db.models import Count, Avg, Q, ExpressionWrapper, F
from django.db.models.functions import TruncMonth, ExtractYear
from registro.models import Registro
import json
from datetime import datetime, timedelta
from django.utils import timezone
import numpy as np
from django.db.models import FloatField

class EstadisticasRegistroView(View):
    """Dashboard de análisis temporal y por estado físico"""

    def get(self, request, *args, **kwargs):
        # 1. Análisis Temporal (Registros por mes)
        registros_mensuales = (
            Registro.objects
            .annotate(mes=TruncMonth('fecha_registro'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )

        # 2. Estado Físico (Distribución)
        estados_fisicos = (
            Registro.objects
            .values('estado_fisico')
            .annotate(
                total=Count('id'),
                avg_edad=Avg('edad'))
            .order_by('-total')
        )

        # 3. Evolución mensual por estado físico
        evolucion_estados = (
            Registro.objects
            .annotate(mes=TruncMonth('fecha_registro'))
            .values('mes', 'estado_fisico')
            .annotate(total=Count('id'))
            .order_by('mes', 'estado_fisico')
        )

        # Preparar datos para gráficos
        meses = sorted(list({r['mes'] for r in evolucion_estados}), key=lambda x: x)
        estados = list({r['estado_fisico'] for r in evolucion_estados})

        # Datos para gráfico de evolución
        datasets = []
        colores = {
            'vivo': '#1cc88a',
            'fallecido': '#e74a3b',
            'en tratamiento': '#f6c23e',
            'recuperado': '#36b9cc'
        }

        for estado in estados:
            data = []
            for mes in meses:
                total = next(
                    (r['total'] for r in evolucion_estados
                     if r['mes'] == mes and r['estado_fisico'] == estado),
                    0
                )
                data.append(total)

            datasets.append({
                'label': estado.capitalize(),
                'data': data,
                'borderColor': colores.get(estado, '#cccccc'),
                'backgroundColor': 'rgba(255, 255, 255, 0.1)',
                'fill': False
            })

        evolucion_data = {
            'labels': [mes.strftime("%b %Y") for mes in meses],
            'datasets': datasets
        }

        # 4. Tasa de Cambio Mensual
        tasa_cambio = self.calcular_tasa_cambio(registros_mensuales)

        # 5. Análisis de Supervivencia (si aplica)
        analisis_supervivencia = self.analizar_supervivencia()

        # Contexto final optimizado
        context = {
            # Datos temporales
            'timeline_labels': [r['mes'].strftime("%b %Y") for r in registros_mensuales],
            'timeline_data': [r['total'] for r in registros_mensuales],

            # Estado físico
            'estados_fisicos': estados_fisicos,
            'estado_fisico_data': {
                'labels': [e['estado_fisico'].capitalize() for e in estados_fisicos],
                'values': [e['total'] for e in estados_fisicos],
                'colors': [
                    '#1cc88a' if e['estado_fisico'] == 'vivo' else
                    '#e74a3b' if e['estado_fisico'] == 'fallecido' else
                    '#f6c23e' for e in estados_fisicos
                ]
            },

            # Evolución
            'evolucion_data_json': json.dumps(evolucion_data),
            'evolucion_data': evolucion_data,  # Envía el diccionario directamente
            # Tasa de cambio
            'tasa_cambio_data': {
                'labels': [t['mes'] for t in tasa_cambio],
                'values': [t['tasa'] for t in tasa_cambio]
            },

            # Supervivencia
            'curva_supervivencia': json.dumps(analisis_supervivencia),

            # Estadísticas resumen
            'stats': {
                'total_registros': Registro.objects.count(),
                'mes_activo': max(registros_mensuales, key=lambda x: x['total']) if registros_mensuales else None,
                'estado_predominante': estados_fisicos[0] if estados_fisicos else None
            }
        }

        return render(request, 'estadisticas_registro.html', context)

    def calcular_tasa_cambio(self, datos_mensuales):
        """Calcula el porcentaje de cambio mes a mes"""
        tasas = []
        for i in range(1, len(datos_mensuales)):
            anterior = datos_mensuales[i - 1]['total']
            actual = datos_mensuales[i]['total']
            cambio = ((actual - anterior) / anterior) * 100 if anterior > 0 else 0
            tasas.append({
                'mes': datos_mensuales[i]['mes'].strftime("%Y-%m"),
                'tasa': round(cambio, 2)
            })
        return tasas

    def analizar_supervivencia(self):
        """Análisis básico de supervivencia (para estados de salud)"""
        if not Registro.objects.filter(estado_fisico='fallecido').exists():
            return None

        # Agrupar por año y calcular proporción de fallecidos
        return (
            Registro.objects
            .annotate(year=ExtractYear('fecha_ingreso'))
            .values('year')
            .annotate(
                total=Count('id'),
                fallecidos=Count('id', filter=Q(estado_fisico='fallecido')),
                tasa=ExpressionWrapper(
                    F('fallecidos') * 100.0 / F('total'),
                    output_field=FloatField()
                )
            )
            .order_by('year')
        )