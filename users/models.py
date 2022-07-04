from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, nick, password, **extra_fields):
        if not email:
            raise ValueError("Users need an email address.")
        if not nick:
            raise ValueError("Users need a nickname.")
        
        user = self.model(email = self.normalize_email(email), nick = nick)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, nick, password, **extra_fields):
        user = self.model(email = self.normalize_email(email), nick = nick)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)

        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name = "email", max_length = 60, unique=True)
    nick = models.CharField(max_length = 30, unique=True)
    date_joined = models.DateTimeField(verbose_name = "date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name = "last joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_img = models.ImageField(upload_to='user_img/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick',]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True