import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0024_meyoriyhujjat_proxy"),
    ]

    operations = [
        migrations.CreateModel(
            name="IlmiyBolim",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("description_uz", models.TextField(blank=True, verbose_name="Bo'lim haqida (Uz)")),
                ("description_ru", models.TextField(blank=True, verbose_name="Bo'lim haqida (Ru)")),
                ("description_en", models.TextField(blank=True, verbose_name="Bo'lim haqida (En)")),
            ],
            options={
                "verbose_name": "Ilmiy bo'lim",
                "verbose_name_plural": "Ilmiy bo'lim",
                "db_table": "pages_ilmiy_bolim",
            },
        ),
        migrations.CreateModel(
            name="IlmiyBolimYonalish",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("text_uz", models.TextField(verbose_name="Yo'nalish (Uz)")),
                ("text_ru", models.TextField(blank=True, verbose_name="Yo'nalish (Ru)")),
                ("text_en", models.TextField(blank=True, verbose_name="Yo'nalish (En)")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Tartib")),
                (
                    "bolim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="yonalishlar",
                        to="pages.ilmiybolim",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ilmiy bo'lim yo'nalishi",
                "verbose_name_plural": "Ilmiy bo'lim yo'nalishlari",
                "db_table": "pages_ilmiy_bolim_yonalish",
                "ordering": ["order"],
            },
        ),
    ]
