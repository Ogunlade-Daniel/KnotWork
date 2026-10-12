from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('Knot', '0014_repair_community_support_constraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitypost',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='community/images/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='communitypost',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.CreateModel(
            name='CommunityPollOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_options', to='Knot.communitypost')),
            ],
            options={'ordering': ('id',)},
        ),
        migrations.CreateModel(
            name='CommunityPollVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='Knot.communitypolloption')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_votes', to='Knot.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_poll_votes', to='auth.user')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('post', 'user'), name='unique_community_poll_vote')],
            },
        ),
    ]