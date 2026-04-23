from django.db import migrations, models
import django.db.models.deletion
import domains.international.models.rating


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0003_internationalpostimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternationalRating',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title_uz', models.CharField(max_length=300, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (En)')),
                ('description_uz', models.TextField(verbose_name='Matn (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Matn (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Matn (En)')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=domains.international.models.rating.rating_cover_upload, verbose_name='Muqova rasmi')),
                ('slug', models.SlugField(blank=True, max_length=350, unique=True)),
                ('date', models.DateField(verbose_name='Sana')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Xalqaro reyting',
                'verbose_name_plural': 'Xalqaro reytinglar',
                'db_table': 'international_rating',
                'ordering': ['-date', 'order'],
            },
        ),
        migrations.CreateModel(
            name='InternationalRatingImage',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=domains.international.models.rating.rating_image_upload, verbose_name='Rasm')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='international.internationalrating', verbose_name='Reyting')),
            ],
            options={
                'verbose_name': 'Reyting rasmi',
                'verbose_name_plural': 'Reyting rasmlari',
                'db_table': 'international_rating_image',
                'ordering': ['order'],
            },
        ),
    ]
