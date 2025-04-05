from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.utils import timezone


# Create your models here.

# class CustomUserManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         if not email:
#             raise ValueError("You have not provided a valid e-mail address.")
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
#
#     def create_user(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)
#
#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(username, email, password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(blank=True, default='', unique=True)
#     name = models.CharField(max_length=255, blank=True, default='')
#
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#
#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#
#     def get_full_name(self):
#         return self.name
#
#     def get_short_name(self):
#         return self.name or self.email.split('@')[0]


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        CLEANER = "CLEANER", "Cleaner"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        help_text="Required. Select an account type.",
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: "
                "'+999999999'. Up to 15 digits allowed.",
            )
        ],
    )
    rating = models.IntegerField(null=True)
    objects = UserManager()


class CleanerAvailability(models.Model):
    cleaner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="availabilities"
    )
    date = models.DateField()
    available_hours = models.JSONField(default=list)

    class Meta:
        unique_together = ("cleaner", "date")

    def day_of_week(self):
        return self.date.strftime("%A")  # Returns 'Monday', 'Tuesday', etc.
