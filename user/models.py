from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    first_user_name,
                    last_user_name,
                    gender,
                    nationality,
                    province,
                    district,
                    city,
                    profession,
                    provenance,
                    birthday,
                    contact,
                    password=None):
        if not email:
            raise ValueError('Users myst have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_user_name=first_user_name,
            last_user_name=last_user_name,
            gender=gender,
            nationality=nationality,
            province=province,
            district=district,
            city=city,
            profession=profession,
            provenance=provenance,
            birthday=birthday,
            contact=contact
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         first_user_name,
                         last_user_name,
                         gender,
                         nationality,
                         province,
                         district,
                         city,
                         profession,
                         provenance,
                         birthday,
                         contact,
                         password=None):
        user = self.create_user(
            email,
            first_user_name,
            last_user_name,
            gender,
            nationality,
            province,
            district,
            city,
            profession,
            provenance,
            birthday,
            contact,
            password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_user_name = models.CharField(max_length=128, blank=True)
    last_user_name = models.CharField(max_length=128, blank=True)
    gender = models.CharField(max_length=32, null=True)
    nationality = models.CharField(max_length=64, default="Moçambique")
    province = models.CharField(max_length=64, default="Maputo")
    district = models.CharField(max_length=64, default="Kaphumo")
    city = models.CharField(max_length=64, default="Maputo")
    profession = models.CharField(max_length=258)
    provenance = models.CharField(max_length=258)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField('auth.Group')
    date_joined = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(null=True, blank=True, default=None)
    contact = models.CharField(max_length=32, null=True, blank=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_user_name',
        'last_user_name',
        'gender',
        'nationality',
        'province',
        'district',
        'city',
        'profession',
        'provenance',
        'birthday',
        'contact'
    ]

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """ Checks if the user has the user permissions """
        return True

    def has_module_perms(self, app_label):
        """ Checks if the user has module permission """
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def first_name(self):
        return self.first_user_name

    @property
    def last_name(self):
        return self.last_user_name


class Code(models.Model):
    email = models.EmailField(unique=True, null=False)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.code}'

    class Meta:
        db_table = 'code'
