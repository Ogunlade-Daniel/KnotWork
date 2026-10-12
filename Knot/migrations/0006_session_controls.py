from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('Knot', '0005_learning_records')]

    operations = [
        migrations.AddField(
            model_name='learningsession', name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='learningsession', name='is_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='learningsession', name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SessionHand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asked_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raised_hands', to='Knot.learningsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raised_hands', to='Knot.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='sessionhand',
            constraint=models.UniqueConstraint(fields=('session', 'student'), name='unique_active_session_hand'),
        ),
    ]