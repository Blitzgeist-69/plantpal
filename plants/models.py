from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
