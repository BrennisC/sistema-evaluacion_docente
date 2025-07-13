from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from apps.usuarios.models import Usuario


from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")

        error = None
        try:
            # Primero verificamos si existe el usuario
            usuario = Usuario.objects.get(correo=correo)
            # Usamos authenticate con correo
            user = authenticate(request, correo=correo, password=password)

            if user is not None:
                # Login exitoso
                login(request, user)  # Iniciamos la sesión del usuario

                if str(usuario.rol) == "comision":
                    url = reverse(
                        "comision:bienvenida_comision",
                        kwargs={"usuario_id": usuario.id},
                    )
                    return redirect(url)
                elif str(usuario.rol) == "profesor":
                    url = reverse(
                        "docente:bienvenido_docente",
                        kwargs={"usuario_id": usuario.id},
                    )
                    return redirect(url)
                elif str(usuario.rol) == "alumno":
                    url = reverse(
                        "alumno:bienvenida_alumno",
                        kwargs={"usuario_id": usuario.id},
                    )
                    return redirect(url)
                else:
                    error = "Rol no reconocido. Contacta con el administrador."
            else:
                error = "Contraseña incorrecta"

        except Usuario.DoesNotExist:
            error = "Usuario no encontrado"

        return render(request, "login.html", {"form": {}, "error": error})

    # Si es GET
    return render(request, "login.html", {"form": {}})


def logout_view(request):
    logout(request)  # Usamos la función logout de Django
    return redirect("core:dashboard")


def dashboard_view(request):
    return render(request, "dashboard_main.html")
