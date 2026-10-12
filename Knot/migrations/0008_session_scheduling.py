from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('Knot', '0007_studio_recordings')]

    operations = [
        migrations.AddField(model_name='learningsession', name='description', field=models.TextField(blank=True, default='')),
        migrations.AddField(model_name='learningsession', name='room_id', field=models.CharField(blank=True, max_length=64, null=True, unique=True)),
        migrations.AddField(model_name='learningsession', name='session_type', field=models.CharField(choices=[('one_to_one', '1-on-1 Video call'), ('group', 'Group call'), ('cohort', 'Cohort class')], default='one_to_one', max_length=20)),
        migrations.AlterField(model_name='learningsession', name='status', field=models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('live', 'Live'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
        migrations.CreateModel(
            name='SessionAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent')], default='absent', max_length=12)),
                ('join_time', models.DateTimeField(blank=True, null=True)),
                ('leave_time', models.DateTimeField(blank=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='Knot.learningsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_attendance', to='Knot.student')),
            ],
        ),
        migrations.CreateModel(
            name='SessionNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='')),
                ('is_private', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_notes', to='Knot.learningsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_notes', to='auth.user')),
            ],
        ),
        migrations.AddConstraint(model_name='sessionattendance', constraint=models.UniqueConstraint(fields=('session', 'student'), name='unique_session_attendance')),
        migrations.AddConstraint(model_name='sessionnote', constraint=models.UniqueConstraint(fields=('session', 'user'), name='unique_session_note_author')),
    ]