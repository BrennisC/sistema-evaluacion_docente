from os import name
from django.urls import path
from . import views


# definir el app name
app_name = "comision"

urlpatterns = [
    # URLs para gestión de periodos de evaluación
    path(
        "gestionar_periodos/<int:usuario_id>/",
        views.gestionar_periodos,
        name="gestionar_periodos",
    ),
    path(
        "crear_periodo/<int:usuario_id>/",
        views.crear_periodo,
        name="crear_periodo",
    ),
    path(
        "configurar_periodo/<int:usuario_id>/<uuid:periodo_id>/",
        views.configurar_periodo,
        name="configurar_periodo",
    ),
    path(
        "seleccionar_tipo_encuesta/<int:usuario_id>/<uuid:periodo_id>/",
        views.seleccionar_tipo_encuesta,
        name="seleccionar_tipo_encuesta",
    ),
    # URL modificada para permitir pasar un periodo_id opcional
    path(
        "realizar_encuesta/<int:usuario_id>/",
        views.realizar_encuesta,
        name="realizar_encuesta",
    ),
    path(
        "realizar_encuesta/<int:usuario_id>/<uuid:periodo_id>/",
        views.realizar_encuesta,
        name="realizar_encuesta_periodo",
    ),
    # URLs existentes
    path(
        "perfil_comision/<int:usuario_id>/",
        views.perfil_comision,
        name="perfil_comision",
    ),
    path(
        "editar_pregunta/<int:usuario_id>/<uuid:id_pregunta>/",
        views.editar_pregunta,
        name="editar_pregunta",
    ),
    path(
        "eliminar_pregunta/<int:usuario_id>/<uuid:id_pregunta>/",
        views.eliminar_pregunta,
        name="eliminar_pregunta",
    ),
    path(
        "agregar_pregunta/<int:usuario_id>/<uuid:id_modulo>/",
        views.agregar_pregunta,
        name="agregar_pregunta",
    ),
    path("bienvenida/<int:usuario_id>/", views.index, name="bienvenida_comision"),
    path(
        "reporte_general/<int:usuario_id>/",
        views.reporter_general,
        name="reporte_general",
    ),
    path("reporte_curso/<int:usuario_id>/", views.reporte_curso, name="reporte_curso"),
    path(
        "reporte_docente/<int:usuario_id>/",
        views.reporte_docente,
        name="reporte_docente",
    ),
]
