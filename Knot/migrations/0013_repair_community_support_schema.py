from django.db import migrations, models


MODEL_NAMES = (
    'CommunityPost',
    'CommunityReply',
    'CommunityReaction',
    'CommunityBookmark',
    'SupportTicket',
    'HelpfulnessFeedback',
)


def repair_schema(apps, schema_editor):
    connection = schema_editor.connection
    existing_tables = {name.casefold() for name in connection.introspection.table_names()}

    for model_name in MODEL_NAMES:
        model = apps.get_model('Knot', model_name)
        table_name = model._meta.db_table
        if table_name.casefold() not in existing_tables:
            continue

        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(cursor, table_name)

        for field in model._meta.local_fields:
            if field.is_relation and field.many_to_one and field.db_constraint:
                target = (field.remote_field.model._meta.db_table, field.target_field.column)
                has_foreign_key = any(
                    info.get('foreign_key')
                    and tuple(value.casefold() for value in info['foreign_key']) == tuple(value.casefold() for value in target)
                    for info in constraints.values()
                )
                if not has_foreign_key:
                    schema_editor.execute(schema_editor._create_fk_sql(model, field, '_fk'))

            if field.db_index and not field.primary_key:
                has_index = any(
                    info.get('index') and info.get('columns') == [field.column]
                    for info in constraints.values()
                )
                if not has_index:
                    index_name = schema_editor._create_index_name(table_name, [field.column])
                    schema_editor.add_index(
                        model,
                        models.Index(fields=[field.name], name=index_name),
                    )

        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(cursor, table_name)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    atomic = False
    dependencies = [('Knot', '0012_communitypost_supportticket_helpfulnessfeedback_and_more')]

    operations = [migrations.RunPython(repair_schema, noop_reverse)]
