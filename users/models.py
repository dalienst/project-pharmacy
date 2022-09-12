from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.abstracts import TimeStampedModel, UniversalIdModel


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, username: str, email: str, password: str, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, UniversalIdModel):
    """
    User model
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"


class Manufacturer(TimeStampedModel, UniversalIdModel):
    """
    Manufacturer model
    """

    manufacturer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="manufacturer"
    )
    company_name = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    license = models.CharField(max_length=255, blank=False, null=False)
    contact = models.BigIntegerField(
        _("phone number"), default=0, unique=True, blank=False
    )

    def __str__(self):
        return self.company_name


class Customer(TimeStampedModel, UniversalIdModel):
    """
    Customer model
    """

    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer"
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    contact = models.BigIntegerField(
        _("phone number"), default=0, unique=True, blank=False
    )
    location = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.first_name


class Pharmacist(TimeStampedModel, UniversalIdModel):
    """ "
    Employee model
    """

    pharmacist = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="pharmacist"
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    contact = models.BigIntegerField(
        _("phone number"), default=0, unique=True, blank=False
    )
    employee_number = models.CharField(max_length=40)

    def __str__(self):
        return self.pharmacist.username
