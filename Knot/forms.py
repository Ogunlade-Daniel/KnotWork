from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Course


class OnboardingForm(forms.Form):
    REQUIRED_ROLE_FIELDS = {
        'student': ('first_name', 'surname', 'email', 'phone_number', 'password', 'confirm_password', 'skill_level', 'learning_goal', 'hear_about_us', 'timezone', 'terms_accepted'),
        'teacher': ('first_name', 'surname', 'email', 'phone_number', 'password', 'confirm_password', 'years_experience', 'current_job_title', 'teaching_style', 'languages_spoken', 'payment_method', 'timezone', 'availability', 'teacher_terms_accepted', 'background_check_consent'),
        'mentor': ('first_name', 'surname', 'email', 'phone_number', 'password', 'confirm_password', 'mentorship_areas', 'industry_skills', 'years_experience', 'current_role_company', 'mentor_bio', 'mentorship_type', 'session_rate', 'availability', 'languages_spoken', 'max_students_per_month', 'mentor_terms_accepted'),
    }
    PROFILE_FIELDS = (
        'first_name', 'surname', 'email', 'short_bio',
        'mentor_bio', 'timezone', 'hear_about_us', 'terms_accepted',
        'email_marketing',
    )

    role = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=80)
    surname = forms.CharField(max_length=80)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=25)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    learning_goal = forms.CharField(max_length=255, required=False)
    skill_level = forms.CharField(max_length=30, required=False)
    hear_about_us = forms.CharField(max_length=100, required=False)
    terms_accepted = forms.BooleanField(required=False)
    email_marketing = forms.BooleanField(required=False)
    timezone = forms.CharField(max_length=100, required=False)
    primary_subject = forms.CharField(max_length=255, required=False)
    years_experience = forms.IntegerField(min_value=0, required=False)
    current_job_title = forms.CharField(max_length=150, required=False)
    portfolio_url = forms.URLField(required=False)
    linkedin_url = forms.URLField(required=False)
    github_url = forms.URLField(required=False)
    short_bio = forms.CharField(required=False, widget=forms.Textarea)
    id_certificate = forms.FileField(required=False)
    teaching_style = forms.CharField(max_length=150, required=False)
    languages_spoken = forms.CharField(max_length=255, required=False)
    payment_method = forms.CharField(max_length=80, required=False)
    availability = forms.CharField(max_length=150, required=False)
    teacher_terms_accepted = forms.BooleanField(required=False)
    background_check_consent = forms.BooleanField(required=False)
    mentorship_areas = forms.CharField(max_length=255, required=False)
    industry_skills = forms.CharField(max_length=255, required=False)
    current_role_company = forms.CharField(max_length=180, required=False)
    mentor_bio = forms.CharField(required=False, widget=forms.Textarea)
    mentor_links = forms.CharField(max_length=500, required=False)
    mentorship_type = forms.CharField(max_length=100, required=False)
    session_rate = forms.CharField(max_length=80, required=False)
    max_students_per_month = forms.IntegerField(min_value=1, required=False)
    mentor_id = forms.FileField(required=False)
    references = forms.CharField(required=False, widget=forms.Textarea)
    mentor_terms_accepted = forms.BooleanField(required=False)

    def clean_role(self):
        role = self.cleaned_data['role']
        if role not in self.REQUIRED_ROLE_FIELDS:
            raise forms.ValidationError('Choose a valid account type.')
        return role

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', 'Passwords do not match.')

        role = cleaned_data.get('role')
        for field_name in self.REQUIRED_ROLE_FIELDS.get(role, ()):
            if not cleaned_data.get(field_name):
                self.add_error(field_name, 'This field is required.')
        if role == 'student' and not cleaned_data.get('terms_accepted'):
            self.add_error('terms_accepted', 'You must accept the terms and privacy policy.')
        if role == 'teacher':
            for field_name in ('teacher_terms_accepted', 'background_check_consent'):
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, 'This consent is required.')
        if role == 'mentor' and not cleaned_data.get('mentor_terms_accepted'):
            self.add_error('mentor_terms_accepted', 'You must accept the mentor terms.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(
            username=cleaned_data.get('email'),
            password=cleaned_data.get('password'),
        )
        if user is None:
            raise forms.ValidationError('Email or password is incorrect.')
        cleaned_data['user'] = user
        return cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'category', 'level', 'description', 'price')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your course a clear, memorable title',
            }),
            'category': forms.Select(),
            'level': forms.Select(),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'What will learners be able to do after this course?',
            }),
            'price': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',
                'placeholder': '0 for free',
            }),
        }