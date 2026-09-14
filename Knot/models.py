from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')

    class Meta:
        managed = True
        db_table = 'Student'


class OnboardingProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True) # index for speed

    # Shared registration fields.
    first_name = models.CharField(max_length=80, blank=True)
    surname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True)
    hear_about_us = models.CharField(max_length=100, blank=True)
    terms_accepted = models.BooleanField(default=False)
    email_marketing = models.BooleanField(default=False)

    # Student fields
    learning_goal = models.CharField(max_length=255, blank=True, null=True)
    skill_level = models.CharField(max_length=30, blank=True, null=True)
    primary_subject = models.CharField(max_length=255, blank=True)
 
    # Teacher fields
    years_experience = models.PositiveSmallIntegerField(null=True, blank=True)
    current_job_title = models.CharField(max_length=150, blank=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    short_bio = models.TextField(blank=True)
    id_certificate = models.FileField(upload_to='media/onboarding/teacher/', blank=True, null=True)
    teaching_style = models.CharField(max_length=150, blank=True)
    languages_spoken = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=80, blank=True)
    availability = models.CharField(max_length=150, blank=True)
    teacher_terms_accepted = models.BooleanField(default=False)
    background_check_consent = models.BooleanField(default=False)

    # Mentor fields
    mentorship_areas = models.CharField(max_length=255, blank=True)
    industry_skills = models.CharField(max_length=255, blank=True)
    current_role_company = models.CharField(max_length=180, blank=True)
    mentor_bio = models.TextField(blank=True)
    mentor_links = models.CharField(max_length=500, blank=True)
    mentorship_type = models.CharField(max_length=100, blank=True)
    session_rate = models.CharField(max_length=80, blank=True)
    max_students_per_month = models.PositiveSmallIntegerField(null=True, blank=True)
    mentor_id = models.FileField(upload_to='onboarding/mentor/', blank=True, null=True)
    references = models.TextField(blank=True)
    mentor_terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
