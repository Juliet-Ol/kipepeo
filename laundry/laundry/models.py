from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class LaundryItem(models.Model):
    """Model representing a laundry item."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    is_washed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} ({'Washed' if self.is_washed else 'Unwashed'})"
    class Meta:
        verbose_name = "Laundry Item"
        verbose_name_plural = "Laundry Items"
        ordering = ['-date_added']
class LaundryLog(models.Model):
    """Model representing a log entry for laundry actions."""
    item = models.ForeignKey(LaundryItem, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # e.g., 'added', 'washed', 'removed'
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} - {self.item.item_name} at {self.timestamp}"
    
    class Meta:
        verbose_name = "Laundry Log"
        verbose_name_plural = "Laundry Logs"
        ordering = ['-timestamp']
class UserProfile(models.Model):
    """Model representing a user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile when the User is saved."""
    instance.userprofile.save()
# laundry/laundry/models.py
# This file contains the models for the laundry application.
# Models include LaundryItem, LaundryLog, and UserProfile.
# Each model represents a table in the database with fields and relationships.
# The LaundryItem model tracks individual laundry items, their status, and the user who owns them.

# The LaundryLog model records actions taken on laundry items, such as adding or washing.
# The UserProfile model extends the User model to include additional user information.
# Signals are used to automatically create and save user profiles when a User is created or updated.
# This ensures that every user has a corresponding profile without manual intervention.
# The models are designed to be used with Django's ORM, allowing for easy database interactions.
# The models are registered with the Django admin interface for easy management.
