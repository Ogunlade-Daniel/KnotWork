from django.conf import settings
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class LiveRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('voice', 'Voice Call'),
        ('video', 'Video Call'),
        ('study', 'Study Circle'),
        ('mentor', 'Mentor Session'),
    ]

    title = models.CharField(max_length=180)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    host_name = models.CharField(max_length=120)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='voice')
    description = models.TextField()
    join_url = models.URLField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at', 'title']
        verbose_name = 'Live Room'
        verbose_name_plural = 'Live Rooms'

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5)
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.author_name} - {self.rating} stars"


class Donation(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        return f"{self.name} donated ${self.amount}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.subject} from {self.name}"

