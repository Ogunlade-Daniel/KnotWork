from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('Knot', '0010_people_request')]

    operations = [
        migrations.AddField(
            model_name='peoplerequest',
            name='responded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='peoplerequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('accepted', 'Accepted'),
                    ('declined', 'Declined'),
                    ('withdrawn', 'Withdrawn'),
                    ('passed', 'Passed'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
    ]