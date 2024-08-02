from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
