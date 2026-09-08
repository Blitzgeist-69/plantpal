from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Plant(models.Model):
    """ A houseplant owned by a user. """

    LIGHT_CHOICES = [
        ('low', 'Low light'),
        ('medium', 'Medium light'),
        ('bright', 'Bright indirect light'),
        ('direct', 'Direct sunlight'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='plants',
    )
    nickname = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text=(
            'Optional: Where the plant is located, e.g Kitchen windowsill.'
        ),
    )
    acquired_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date plant acquired.',
    )
    water_frequency_days = models.PositiveIntegerField(
        default=7,
        help_text='How often to water the plant, in days.',
    )
    light_needs = models.CharField(
        max_length=25,
        choices=LIGHT_CHOICES,
        default='medium',
        help_text='Plant light requirements.',
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about the plant.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nickname']

    def __str__(self):
        return f"{self.nickname} ({self.species})"

    def get_absolute_url(self):
        return reverse('plants:plant_detail', args=[self.pk])

    def last_watered_date(self):
        """Most recent Watered log, or None if never watered."""
        latest = self.care_logs.filter(action='water').first()
        if latest is None:
            return None
        return latest.date

    def due_date(self):
        """
        Date watering is next due or if never watered due today - needs attention.
        """
        last = self.last_watered_date()
        if last is None:
            return timezone.localdate()
        return last + timedelta(days=self.water_frequency_days)

    def needs_attention(self):
        """ Return True if the plant is due for care today or earlier. """
        return self.due_date() <= timezone.localdate()


class CareLog(models.Model):
    """ A log entry for a plant care activity. """

    ACTION_CHOICES = [
        ('water', 'Watered'),
        ('fertilize', 'Fertilized'),
        ('prune', 'Pruned'),
        ('repot', 'Repotted'),
        ('check', 'Health check'),
        ('other', 'Other'),
    ]

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name='care_logs',
    )
    date = models.DateField()
    action = models.CharField(max_length=25, choices=ACTION_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return (
            f'{self.get_action_display()} - {self.plant.nickname} '
            f'on {self.date}'
        )
