from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Model for user account, inheriting AbstractUser.
    Adds additional fields such as user type (is_customer, is_employee)
    and phone number (phone).
    """
    is_customer = models.BooleanField(null=False) # flag indicating whether the user is a customer
    is_employee = models.BooleanField(null=False) # flag indicating whether the user is a employee
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        """Returns the string representation of the user."""
        return self.username


class Task(models.Model):
    """Model for a task."""
    STATUS_CHOICES = (
        ('WAITING', 'Waiting for assignee'),
        ('IN_PROGRESS', 'In progress'),
        ('COMPLETED', 'Completed'),
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    report = models.TextField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')

    def __str__(self):
        """Returns the string representation of the task."""
        return self.title
