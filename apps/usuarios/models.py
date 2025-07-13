from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from apps.roles.models import Rol, ModosRoles
from django.core.mail import send_mail
import uuid


def get_default_admin_role():
    """Obtiene o crea el rol de administrador por defecto"""
    return Rol.objects.get_or_create(
        nombre=ModosRoles.ADMIN, defaults={"permisos": {}}
    )[0].id


class CustomUserManager(BaseUserManager):
    def _create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)

        # Aseguramos que la contraseña esté hasheada
        if password is not None:
            extra_fields["password"] = make_password(password)

        user = self.model(correo=correo, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(correo, password, **extra_fields)

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser debe tener is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser debe tener is_superuser=True.")

        return self._create_user(correo, password, **extra_fields)


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    correo = models.EmailField(
        "correo electrónico",
        unique=True,
        error_messages={
            "unique": "Ya existe un usuario con este correo.",
        },
    )
    username = models.CharField(
        "nombre de usuario",
        max_length=150,
        unique=True,
        null=True,  # Temporalmente permitimos null
        blank=True,  # Temporalmente permitimos blank
        error_messages={
            "unique": "Ya existe un usuario con ese nombre.",
        },
    )
    nombre = models.CharField("nombre completo", max_length=100)
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="rol del usuario",
        default=get_default_admin_role,  # Establecemos el rol por defecto
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "correo"
    USERNAME_FIELD = "correo"  # Usamos correo para login
    REQUIRED_FIELDS = []  # username es opcional temporalmente

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def save(self, *args, **kwargs):
        if not self.username and self.correo:
            self.username = self.correo.split("@")[0]
        if not self.rol_id:  # Si no tiene rol asignado
            self.rol = Rol.objects.get_or_create(
                nombre=ModosRoles.ADMIN, defaults={"permisos": {}}
            )[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.correo} ({self.rol})"

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envía un email al usuario usando el campo correo."""
        send_mail(subject, message, from_email, [self.correo], **kwargs)
