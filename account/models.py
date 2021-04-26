from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth import get_user_model
#User = get_user_model()

# Create your models here.
class CustomersManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Customers must have an email")
        #if not username:
            #raise ValueError("Customers must have an username")
        user = self.model(
                email=self.normalize_email(email),
                #username=username,
                
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
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            #username=username,
        
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.ein_verified = False
        user.save(using=self._db)
        return user



class Customers(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=70, unique=True)
    username = models.CharField(max_length=30)
    company_name=models.CharField("Business Legal Name", max_length=30)
    first_name = models.CharField("Company Owner's First Name", max_length=30)
    last_name = models.CharField("Company Owner's Last Name", max_length=30)
    stripe_customer = models.CharField(max_length=150) 
    ein = models.CharField(verbose_name="Tax Payer Number", max_length=15, blank=True, null=True, unique=True)
    ein_verified = models.BooleanField(verbose_name="TPN Verified?", default=False)
    phone = PhoneNumberField(null=False, blank=False)
    admin = models.BooleanField(default=False) # a superuser
    staff = models.BooleanField(default=False) # a admin user; non super-user
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomersManager()

    

    def __str__(self):
        return self.email

    
    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"
        ordering = ("date_joined",)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def get_legal_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.company_name

    def email_customer(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        
        '''
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    