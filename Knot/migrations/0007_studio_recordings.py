from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('Knot', '0006_session_controls')]

    operations = [
        migrations.CreateModel(
            name='StudioRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='processing', max_length=20)),
                ('mode', models.CharField(default='camera', max_length=20)),
                ('duration_seconds', models.PositiveIntegerField(default=0)),
                ('size_mb', models.DecimalField(decimal_places=1, default=0, max_digits=9)),
                ('media_url', models.URLField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studio_recordings', to='Knot.course')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recordings', to='Knot.learningsession')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studio_recordings', to='Knot.teacher')),
            ],
            options={'ordering': ('-created_at',)},
        ),
    ]