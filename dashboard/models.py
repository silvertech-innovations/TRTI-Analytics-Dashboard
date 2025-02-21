from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves a user with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # Stores password in plain text 
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Stores plain text password 
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def set_password(self, raw_password):
        """Sets the password as plain text"""
        self.password = raw_password

    def check_password(self, raw_password):
        """Compares the stored password with input"""
        return self.password == raw_password

    def __str__(self):
        return self.email
