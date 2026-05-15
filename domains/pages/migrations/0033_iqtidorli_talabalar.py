import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0032_kampus_xizmati'),
    ]

    operations = [
        migrations.CreateModel(
            name='IqtidorliTalabalar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('boshliq_lavozim_uz', models.CharField(default="Sektor boshlig'i", max_length=200, verbose_name='Lavozim (Uz)')),
                ('boshliq_lavozim_ru', models.CharField(blank=True, max_length=200, verbose_name='Lavozim (Ru)')),
                ('boshliq_lavozim_en', models.CharField(blank=True, max_length=200, verbose_name='Lavozim (En)')),
                ('boshliq_fio_uz', models.CharField(max_length=200, verbose_name='F.I.O (Uz)')),
                ('boshliq_fio_ru', models.CharField(blank=True, max_length=200, verbose_name='F.I.O (Ru)')),
                ('boshliq_fio_en', models.CharField(blank=True, max_length=200, verbose_name='F.I.O (En)')),
                ('qabul_kunlari_uz', models.CharField(blank=True, max_length=200, verbose_name='Qabul kunlari (Uz)')),
                ('qabul_kunlari_ru', models.CharField(blank=True, max_length=200, verbose_name='Qabul kunlari (Ru)')),
                ('qabul_kunlari_en', models.CharField(blank=True, max_length=200, verbose_name='Qabul kunlari (En)')),
                ('telefon', models.CharField(blank=True, max_length=50, verbose_name='Telefon')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('image', models.ImageField(blank=True, null=True, upload_to='iqtidorli/', verbose_name='Rasm')),
                ('bolim_title_uz', models.CharField(default="Bo'lim vazifalari:", max_length=200, verbose_name="Bo'lim sarlavhasi (Uz)")),
                ('bolim_title_ru', models.CharField(blank=True, max_length=200, verbose_name="Bo'lim sarlavhasi (Ru)")),
                ('bolim_title_en', models.CharField(blank=True, max_length=200, verbose_name="Bo'lim sarlavhasi (En)")),
            ],
            options={
                'verbose_name': 'Iqtidorli talabalar (bosh)',
                'verbose_name_plural': 'Iqtidorli talabalar (bosh)',
                'db_table': 'pages_iqtidorli_talabalar',
            },
        ),
        migrations.CreateModel(
            name='IqtidorliVazifa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('text_uz', models.TextField(verbose_name='Matn (Uz)')),
                ('text_ru', models.TextField(blank=True, verbose_name='Matn (Ru)')),
                ('text_en', models.TextField(blank=True, verbose_name='Matn (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('parent', models.ForeignKey(on_delete=models.CASCADE, related_name='vazifalar', to='pages.iqtidorlitalabalar')),
            ],
            options={
                'verbose_name': 'Iqtidorli talabalar vazifasi',
                'verbose_name_plural': 'Iqtidorli talabalar vazifalari',
                'db_table': 'pages_iqtidorli_vazifa',
                'ordering': ['order'],
            },
        ),
    ]
