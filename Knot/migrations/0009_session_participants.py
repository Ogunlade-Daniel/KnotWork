from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('Knot', '0008_session_scheduling')]

    operations = [
        migrations.CreateModel(
            name='SessionParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('host', 'Host'), ('co_host', 'Co-host'), ('student', 'Student'), ('observer', 'Observer')], default='student', max_length=20)),
                ('attendance', models.CharField(choices=[('invited', 'Invited'), ('present', 'Present'), ('late', 'Late'), ('absent', 'Absent')], default='invited', max_length=12)),
                ('joined_at', models.DateTimeField(blank=True, null=True)),
                ('left_at', models.DateTimeField(blank=True, null=True)),
                ('hand_raised', models.BooleanField(default=False)),
                ('hand_raised_at', models.DateTimeField(blank=True, null=True)),
                ('is_muted', models.BooleanField(default=True)),
                ('is_cam_off', models.BooleanField(default=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='Knot.learningsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_participation', to='auth.user')),
            ],
        ),
        migrations.AddConstraint(model_name='sessionparticipant', constraint=models.UniqueConstraint(fields=('session', 'user'), name='unique_session_participant')),
    ]