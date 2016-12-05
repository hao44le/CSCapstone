"""AuthenticationApp Models

Created by Naman Patwari on 10/4/2016.
"""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, first_name=None, last_name=None,contact_info=None,description=None,is_student=None, is_professor=None, is_engineer=None):
        if not email:
            raise ValueError('Users must have an email address')

        #We can safetly create the user
        #Only the email field is required
        user = self.model(email=email)
        user.set_password(password)
        user.last_name = last_name
        #If first_name is not present, set it as email's username by default
        if first_name is None or first_name == "" or first_name == '':
            user.first_name = email[:email.find("@")]

        #Classify the Users as Students, Professors, Engineers
        if is_student == True and is_professor == True and is_engineer == True:
            #hack to set Admin using forms
            user.is_admin = True
        elif is_student == True:
            user.is_student = True
        elif is_professor == True:
            user.is_professor = True
        elif is_engineer == True:
            user.is_engineer = True
        else:
            user.is_admin = True
        user.contact_info = contact_info
        user.description = description
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, first_name=None, last_name=None,contact_info=None,description=None):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name,contact_info=None,description=None,
            is_student=None, is_professor=None, is_engineer=None)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_student(self, email=None, password=None,first_name=None, last_name=None,contact_info=None,description=None):
        return self.create_user(email, password=password,first_name=first_name, last_name=last_name,contact_info=None,description=None,
        is_student=True, is_professor=False, is_engineer=False)

    def create_professor(self, email=None, password=None,first_name=None, last_name=None,contact_info=None,description=None):
        return self.create_user(email, password=password,first_name=first_name, last_name=last_name,contact_info=None,description=None,
        is_student=False, is_professor=True, is_engineer=False)

    def create_engineer(self, email=None, password=None,first_name=None, last_name=None,contact_info=None,description=None):
        return self.create_user(email, password=password,first_name=first_name, last_name=last_name,contact_info=None,description=None,
        is_student=False, is_professor=False, is_engineer=True)

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )

    last_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )
    contact_info = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )
    description = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )

    is_active = models.BooleanField(default=True,)
    is_admin = models.BooleanField(default=False,)

    # #New fields added
    is_student = models.BooleanField(default=False,)
    is_professor = models.BooleanField(default=False,)
    is_engineer = models.BooleanField(default=False,)



    programmingLanguage = models.CharField(max_length=200,default=None,null=True)
    yearsOfExperience = models.IntegerField(default=0,null=True)
    speciality = models.CharField(max_length=200,default=None,null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):              #Python 3
        return self.email

    def __unicode__(self):           # Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin

#     def new_user_reciever(sender, instance, created, *args, **kwargs):
#     	if created:

# Going to use signals to send emails
# post_save.connect(new_user_reciever, sender=MyUser)


class Student(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)

    courses = models.ForeignKey('UniversitiesApp.Course',default=None,null=True)
    groups = models.ForeignKey('GroupsApp.Group',default=None,null=True)
    university = models.OneToOneField('UniversitiesApp.University',default=None,null=True)
    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return False

class Professor(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)
    courses = models.ForeignKey('UniversitiesApp.Course',default=None,null=True)
    university = models.OneToOneField('UniversitiesApp.University',default=None,null=True)
    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return False

class Engineer(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)
    companies = models.ForeignKey('CompaniesApp.Company',default=None,null=True)
    projects = models.ForeignKey('ProjectsApp.Project',default=None,null=True)
    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return False
