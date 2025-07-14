from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario
from apps.roles.models import Rol, ModosRoles


class Command(BaseCommand):
    help = "Crea usuarios de prueba para diferentes roles"

    def handle(self, *args, **kwargs):
        # Lista de usuarios de prueba
        usuarios_prueba = [
            {
                "correo": "admin@test.com",
                "password": "demo12345",
                "nombre": "Administrador de Prueba",
                "rol": ModosRoles.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "correo": "profesor@test.com",
                "password": "demo12345",
                "nombre": "Profesor de Prueba",
                "rol": ModosRoles.PROFESOR,
            },
            {
                "correo": "alumno@test.com",
                "password": "demo12345",
                "nombre": "Alumno de Prueba",
                "rol": ModosRoles.ALUMNO,
            },
            {
                "correo": "comision@test.com",
                "password": "demo12345",
                "nombre": "Comisión de Prueba",
                "rol": ModosRoles.COMISION,
            },
        ]

        for user_data in usuarios_prueba:
            rol_nombre = user_data.pop("rol")
            # Obtener o crear el rol
            rol, _ = Rol.objects.get_or_create(
                nombre=rol_nombre, defaults={"permisos": {}}
            )

            try:
                # Verificar si el usuario ya existe
                if not Usuario.objects.filter(correo=user_data["correo"]).exists():
                    # Crear el usuario usando el manager personalizado
                    usuario = Usuario.objects.create_user(
                        correo=user_data["correo"],
                        password=user_data["password"],
                        nombre=user_data["nombre"],
                        rol=rol,
                        is_staff=user_data.get("is_staff", False),
                        is_superuser=user_data.get("is_superuser", False),
                        is_active=True,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Usuario creado exitosamente: {user_data["correo"]}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'El usuario ya existe: {user_data["correo"]}'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creando usuario {user_data["correo"]}: {str(e)}'
                    )
                )
