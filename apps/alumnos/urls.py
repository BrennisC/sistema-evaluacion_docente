from django.urls import path
from . import views

app_name = "alumno"

urlpatterns = [
    path(
        "bienvenido_alumno/<int:usuario_id>/",
        views.bienvenida_alumnos,
        name="bienvenida_alumno",
    ),
    path("perfil_alumno/<int:usuario_id>/", views.perfil_alumno, name="perfil_alumno"),
    path(
        "evaluaciones/<int:usuario_id>/",
        views.evaluar_docente,
        name="evaluaciones",
    ),
    path("explorar/<int:usuario_id>/", views.explorar, name="explorar"),
    path(
        "detalle_docente/<int:usuario_id>/<int:docente_id>/",
        views.detalle_docente,
        name="detalle_docente",
    ),
]
