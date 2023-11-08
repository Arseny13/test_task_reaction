from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс пользователя."""
    @property
    def is_admin(self):
        """Проверяет, если пользователь Администратор."""
        return self.is_superuser
