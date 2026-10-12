from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Knot', '0004_alter_course_course_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='last_accessed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='progress_percent',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_id', models.CharField(max_length=24, unique=True)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='Knot.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='Knot.student')),
            ],
            options={'ordering': ('-issued_at',)},
        ),
        migrations.CreateModel(
            name='LearningDeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('due_at', models.DateTimeField()),
                ('action_label', models.CharField(default='Open', max_length=40)),
                ('is_completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='Knot.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='Knot.student')),
            ],
            options={'ordering': ('due_at',)},
        ),
        migrations.CreateModel(
            name='LearningSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('starts_at', models.DateTimeField()),
                ('duration_minutes', models.PositiveSmallIntegerField(default=45)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('meeting_url', models.URLField(blank=True, default='')),
                ('notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='learning_sessions', to='Knot.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_sessions', to='Knot.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_sessions', to='Knot.teacher')),
            ],
            options={'ordering': ('starts_at',)},
        ),
        migrations.CreateModel(
            name='SavedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by', to='Knot.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_courses', to='Knot.student')),
            ],
            options={'ordering': ('-saved_at',)},
        ),
        migrations.CreateModel(
            name='WeeklyGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateField()),
                ('target_sessions', models.PositiveSmallIntegerField(default=5)),
                ('completed_sessions', models.PositiveSmallIntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_goals', to='Knot.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='certificate',
            constraint=models.UniqueConstraint(fields=('student', 'course'), name='unique_student_certificate'),
        ),
        migrations.AddConstraint(
            model_name='savedcourse',
            constraint=models.UniqueConstraint(fields=('student', 'course'), name='unique_saved_course'),
        ),
        migrations.AddConstraint(
            model_name='weeklygoal',
            constraint=models.UniqueConstraint(fields=('student', 'week_start'), name='unique_student_weekly_goal'),
        ),
    ]
