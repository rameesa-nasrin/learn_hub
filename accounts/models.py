from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = [
        ("trainer","trainer"),
        ("student","student"),
        ("admin","admin")
    ]

    phone = models.CharField(max_length=12,unique=True)

    role = models.CharField(max_length=100,choices=ROLE_CHOICES,default="student")

class StudentProfile(models.Model):

    skills = models.CharField(max_length=200,null=True) 

    qualification = models.CharField(max_length=200,null=True)

    passout_year = models.CharField(max_length=20,null=True)

    github_url = models.URLField(null=True)

    linkedin_url = models.URLField(null=True)

    student = models.OneToOneField(User,on_delete=models.CASCADE,related_name="student")


class TrainerProfile(models.Model):

    qualification = models.CharField(max_length=100)

    experience = models.PositiveIntegerField()

    skills = models.CharField(max_length=100)

    trainer = models.OneToOneField(User,on_delete=models.CASCADE,related_name="trainer")


from django.db.models.signals import post_save

def create_student_profile(sender,instance,created,*args,**kwargs):

    if created and instance.role == "student":

        StudentProfile.objects.create(student=instance)

    post_save.connect(create_student_profile,sender=User)


def create_trainer_profile(sender,instance,created,*args,**kwargs):

    if created and instance.role == "trainer":

        TrainerProfile.objects.create(trainer=instance)

    post_save.connect(create_student_profile,sender=User)