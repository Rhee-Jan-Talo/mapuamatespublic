from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    class Strands(models.TextChoices):
            STEM = "STEM", _("Science, Technology, Engineering, And Mathematics")
            ABM = "ABM", _("Accountancy, Business, and Management")
            HUMSS = "HUMSS",_("Humanities and Social Sciences")
            TVL = "TVL", _("Technical-Vocational Livelihood")
            ADT = "ADT",_("Arts and Design")
            ICT = "ICT", _("Information and Communications Technology")

    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=255, null=True, blank=True )
    mname = models.CharField(max_length=255, null=True, blank=True )
    lname = models.CharField(max_length=255, null=True, blank=True )
    pfp = models.ImageField(upload_to = 'images', null=True, blank=True)
    strand = models.CharField(max_length=100, choices=Strands.choices, null=True, blank=True)
    objects = UserManager()






    

    
