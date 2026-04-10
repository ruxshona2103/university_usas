"""
Migration: News/Event/Blog → bitta Article jadvali (proxy pattern).

Holat: eski 0002_navbar_items_m2m allaqachon DB ga apply qilingan edi.
Shuning uchun InformationContent qismi uchun SeparateDatabaseAndState ishlatiladi
(Django state ni yangilaymiz, DB ga tegmaymiz).
"""
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        ('pages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        # ── 1. InformationContent: DB da allaqachon o'zgargan — state ni sync qilamiz ──

        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveIndex(
                    model_name='informationcontent',
                    name='news_inform_navbar__053605_idx',
                ),
                migrations.RemoveField(
                    model_name='informationcontent',
                    name='navbar_item',
                ),
                migrations.AddField(
                    model_name='informationcontent',
                    name='navbar_items',
                    field=models.ManyToManyField(
                        blank=True,
                        related_name='information_items',
                        to='pages.navbarsubitem',
                        verbose_name='Navbar sahifalari',
                    ),
                ),
            ],
            database_operations=[],  # DB da allaqachon bajarilgan
        ),

        # ── 2. Eski navbar M2M junction jadvallarini o'chirish ────────────────

        migrations.RunSQL("DROP TABLE IF EXISTS news_news_navbar_items;",    reverse_sql=""),
        migrations.RunSQL("DROP TABLE IF EXISTS news_event_navbar_items;",   reverse_sql=""),
        migrations.RunSQL("DROP TABLE IF EXISTS news_blog_navbar_items;",    reverse_sql=""),

        # ── 3. Article jadvali yaratiladi ─────────────────────────────────────

        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('image', models.ImageField(upload_to='content/%Y/%m/', verbose_name='Asosiy rasm')),
                ('title_uz', models.CharField(max_length=255, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=255, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=255, verbose_name='Sarlavha (En)')),
                ('description_uz', models.TextField(verbose_name='Batafsil (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Batafsil (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Batafsil (En)')),
                ('keywords', models.CharField(blank=True, max_length=500, verbose_name="SEO Kalit so'zlar")),
                ('date', models.DateTimeField(verbose_name='Sana')),
                ('slug', models.SlugField(blank=True, max_length=300, unique=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Saytga chiqarilsinmi?')),
                ('views', models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")),
                ('article_type', models.CharField(
                    choices=[('news', 'Yangilik'), ('event', 'Tadbir'), ('blog', 'Blog')],
                    db_index=True, max_length=10, verbose_name='Tur',
                )),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='Manba')),
                ('location_uz', models.CharField(blank=True, max_length=300, verbose_name='Manzil (Uz)')),
                ('location_ru', models.CharField(blank=True, max_length=300, verbose_name='Manzil (Ru)')),
                ('location_en', models.CharField(blank=True, max_length=300, verbose_name='Manzil (En)')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Boshlanish vaqti')),
                ('author', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='articles',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Muallif',
                )),
            ],
            options={
                'verbose_name': 'Maqola',
                'verbose_name_plural': 'Maqolalar',
                'db_table': 'news_article',
                'ordering': ['-date'],
            },
        ),

        # ── 4. Eski concrete modellar o'chiriladi ─────────────────────────────

        migrations.DeleteModel(name='News'),
        migrations.DeleteModel(name='Event'),
        migrations.DeleteModel(name='Blog'),

        # ── 5. Proxy modellar ro'yxatdan o'tkaziladi (DB da jadval YO'Q) ──────

        migrations.CreateModel(
            name='News',
            fields=[],
            options={
                'verbose_name': 'Yangilik',
                'verbose_name_plural': "Yangiliklar va E'lonlar",
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('news.article',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[],
            options={
                'verbose_name': 'Tadbir',
                'verbose_name_plural': 'Kutilayotgan tadbirlar',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('news.article',),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Bloglar',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('news.article',),
        ),
    ]
