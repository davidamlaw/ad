from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (BaseUserManager,
                                        PermissionsMixin,
                                        AbstractBaseUser)
from PIL import Image

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(PermissionsMixin, AbstractBaseUser):
    username = None
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def admin(self):
        "Is the user a admin member?"
        return self.is_admin

    objects = UserManager()

class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to='media/profile_pics')
    title = models.CharField(max_length=64, blank=True)
    bio = models.TextField(default=None)

    def save(self, *args, **kwargs):

        try:
            super().save()
            img = Image.open(self.profile_pic.path)
            width, height = img.size  # Get dimensions

            if width > 360 and height > 360:
                # keep ratio but shrink down
                img.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off equal amounts top and bottom
                left = 0
                right = width
                top = (height - width) / 2
                bottom = (height + width) / 2
                img = img.crop((left, top, right, bottom))

            if width > 360 and height > 360:
                img.thumbnail((360, 360))

            img.save(self.profile_pic.path)

        except:
            pass

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
