from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password=None):
        user = self.create_user(email, full_name, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[RegexValidator(r'^\+?\d{10,15}$')]
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Used for admin panel access
    is_active = models.BooleanField(default=True)  # Used to deactivate users
    is_office_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

class Classes(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[RegexValidator(r'^\+?\d{10,15}$')]
    )    
    # class_name = models.CharField(max_length=50)
    class_name=models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='Classes_names')
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name


class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='library_histories')
    book_name = models.CharField(max_length=255)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')])


class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees_histories')
    fee_type = models.CharField(max_length=50, choices=[('library_fee', 'Library Fee')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)