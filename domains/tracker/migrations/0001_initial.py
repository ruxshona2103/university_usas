from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=255)),
                ('view_token', models.UUIDField(db_index=True)),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='contenttypes.contenttype',
                )),
            ],
            options={
                'verbose_name': "Ko'rish",
                'verbose_name_plural': "Ko'rishlar",
                'db_table': 'tracker_content_view',
            },
        ),
        migrations.AlterUniqueTogether(
            name='contentview',
            unique_together={('content_type', 'object_id', 'view_token')},
        ),
    ]
