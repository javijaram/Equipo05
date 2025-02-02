from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


#clase para los roles
class Role(models.Model):
    """ 
    @class Role
    @extends models.Model
    @description Modelo de Rol para gestionar roles dinámicos. Este modelo incluye un nombre de rol único y una relación ManyToMany con permisos.
    """
    name = models.CharField(max_length=50, unique=True)  # Nombre del rol
    permissions = models.ManyToManyField(Permission, blank=True)  # Permisos asociados al rol

    def __str__(self):
        """
        @method __str__
        @description Retorna el nombre del rol como representación en string del modelo.
        @returns {str} El nombre del rol.
        """
        return self.name

#clase de usuario modificado
class CustomUser(AbstractUser):
    """
    @class CustomUser
    @extends AbstractUser
    @description Modelo de usuario personalizado que extiende la clase AbstractUser de Django. Este modelo incluye un campo de correo electrónico único y una relación ManyToMany con el modelo de roles, permitiendo asignar múltiples roles a cada usuario.
    """
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')  # Relación con roles

    def __str__(self):
        """
        @method __str__
        @description Retorna el nombre de usuario como representación en string del modelo.
        @returns {str} El nombre de usuario.
        """

        return self.username

    def has_role(self, role_name):
        """
        @method has_role
        @description Comprueba si el usuario tiene un rol específico.
        @param {str} role_name - El nombre del rol a comprobar.
        @returns {bool} Verdadero si el usuario tiene el rol, Falso en caso contrario.
        """
        return self.roles.filter(name=role_name).exists()

    def get_permissions(self):
        """
        @method get_permissions
        @description Obtiene todos los permisos asociados a los roles del usuario.
        @returns {set} Un conjunto de codenames de permisos.
        """
        permissions = super().get_user_permissions()
        for role in self.roles.all():
            permissions |= set(role.permissions.values_list('codename', flat=True))
        return permissions
    





    








