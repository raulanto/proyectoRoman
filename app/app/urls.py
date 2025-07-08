"""
    Sistema FRH - URLs Configuration

"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from registro.views import Index,Edades,EstadisticasRegistroView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("home/", Index.as_view(), name="home", kwargs={"login_required": True}),
    path("edades/", Edades.as_view(), name="edades", kwargs={"login_required": True}),
    path("poblacion/", EstadisticasRegistroView.as_view(), name="poblacion", kwargs={"login_required": True}),


]
