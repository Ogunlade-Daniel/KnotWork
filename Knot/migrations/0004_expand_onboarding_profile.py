from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Knot', '0003_onboardingprofile_email_onboardingprofile_full_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(model_name='onboardingprofile', name='full_name'),
        migrations.AddField(model_name='onboardingprofile', name='first_name', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='onboardingprofile', name='surname', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='onboardingprofile', name='hear_about_us', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='onboardingprofile', name='terms_accepted', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='onboardingprofile', name='email_marketing', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='onboardingprofile', name='current_job_title', field=models.CharField(blank=True, max_length=150)),
        migrations.AddField(model_name='onboardingprofile', name='portfolio_url', field=models.URLField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='linkedin_url', field=models.URLField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='github_url', field=models.URLField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='short_bio', field=models.TextField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='id_certificate', field=models.FileField(blank=True, null=True, upload_to='onboarding/teacher/')),
        migrations.AddField(model_name='onboardingprofile', name='teaching_style', field=models.CharField(blank=True, max_length=150)),
        migrations.AddField(model_name='onboardingprofile', name='languages_spoken', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='onboardingprofile', name='payment_method', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='onboardingprofile', name='teacher_terms_accepted', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='onboardingprofile', name='background_check_consent', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='onboardingprofile', name='industry_skills', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='onboardingprofile', name='current_role_company', field=models.CharField(blank=True, max_length=180)),
        migrations.AddField(model_name='onboardingprofile', name='mentor_bio', field=models.TextField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='mentor_links', field=models.CharField(blank=True, max_length=500)),
        migrations.AddField(model_name='onboardingprofile', name='mentorship_type', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='onboardingprofile', name='session_rate', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='onboardingprofile', name='max_students_per_month', field=models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField(model_name='onboardingprofile', name='mentor_id', field=models.FileField(blank=True, null=True, upload_to='onboarding/mentor/')),
        migrations.AddField(model_name='onboardingprofile', name='references', field=models.TextField(blank=True)),
        migrations.AddField(model_name='onboardingprofile', name='mentor_terms_accepted', field=models.BooleanField(default=False)),
        migrations.AlterField(model_name='onboardingprofile', name='skill_level', field=models.CharField(blank=True, max_length=30, null=True)),
        migrations.AlterField(model_name='onboardingprofile', name='availability', field=models.CharField(blank=True, max_length=150)),
        migrations.RemoveField(model_name='onboardingprofile', name='mentor_motivation'),
        migrations.RemoveField(model_name='onboardingprofile', name='experience'),
    ]