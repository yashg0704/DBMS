from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Faculty, Student

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the user is associated with a Faculty or Student instance
        if hasattr(instance, 'faculty'):
            UserProfile.objects.create(user=instance, role='faculty')
        elif hasattr(instance, 'student'):
            UserProfile.objects.create(user=instance, role='student')
        else:
            # Assign default role as student if no specific relation is found
            UserProfile.objects.create(user=instance, role='student')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
