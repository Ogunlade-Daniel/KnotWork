from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class CreateModelIfMissing(migrations.CreateModel):
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.name)
        table_names = {name.casefold() for name in schema_editor.connection.introspection.table_names()}
        if model._meta.db_table.casefold() in table_names:
            return
        super().database_forwards(app_label, schema_editor, from_state, to_state)


class AddConstraintIfMissing(migrations.AddConstraint):
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        with schema_editor.connection.cursor() as cursor:
            constraints = schema_editor.connection.introspection.get_constraints(cursor, model._meta.db_table)
        if self.constraint.name in constraints:
            return
        super().database_forwards(app_label, schema_editor, from_state, to_state)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Knot', '0011_people_request_resolution'),
    ]

    operations = [
        CreateModelIfMissing(
            name='CommunityPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('body', models.TextField()),
                ('category', models.CharField(choices=[('discussion', 'Discussion'), ('question', 'Question'), ('showcase', 'Showcase'), ('feedback', 'Feedback'), ('jobs', 'Opportunities'), ('announce', 'Announcement')], db_index=True, default='discussion', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('-created_at',)},
        ),
        CreateModelIfMissing(
            name='SupportTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='general', max_length=40)),
                ('subject', models.CharField(max_length=180)),
                ('message', models.TextField(max_length=5000)),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In progress'), ('resolved', 'Resolved'), ('closed', 'Closed')], db_index=True, default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('-updated_at',)},
        ),
        CreateModelIfMissing(
            name='HelpfulnessFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(default='help-centre', max_length=80)),
                ('was_helpful', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helpfulness_feedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        CreateModelIfMissing(
            name='CommunityReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=3000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_replies', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Knot.communitypost')),
            ],
            options={'ordering': ('created_at',)},
        ),
        CreateModelIfMissing(
            name='CommunityReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='Knot.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_reactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        CreateModelIfMissing(
            name='CommunityBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='Knot.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('-created_at',)},
        ),
        AddConstraintIfMissing(
            model_name='helpfulnessfeedback',
            constraint=models.UniqueConstraint(fields=('user', 'topic'), name='unique_helpfulness_feedback'),
        ),
        AddConstraintIfMissing(
            model_name='communityreaction',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_community_reaction'),
        ),
        AddConstraintIfMissing(
            model_name='communitybookmark',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_community_bookmark'),
        ),
    ]
