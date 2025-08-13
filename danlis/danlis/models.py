from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users harus memiliki email address')
        if not username:
            raise ValueError('Users harus memiliki username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)   

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User model to extend the default Django User model.
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_staff = models.BooleanField(default=False)       # ← WAJIB
    is_active = models.BooleanField(default=True)       # ← WAJIB
    date_joined = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.username
    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.last_name}".strip() or self.username

class Dataset(models.Model):
    namaFile = models.CharField(max_length=255)
    tanggalUpload = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.namaFile} "
    
class Transaction(models.Model):
    """
    Model to store transaction data.
    """
    nama = models.CharField(max_length=150)
    item = models.CharField(max_length=255)
    tanggal= models.DateTimeField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nama.username} - {self.item}"
    
