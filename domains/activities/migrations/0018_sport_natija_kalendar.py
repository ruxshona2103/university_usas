import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0017_ilmiyjurnal_ilmiykengashseminar_ilmiykontentsahifa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportNatija',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('bosqich', models.CharField(choices=[('1', '1-bosqich'), ('2', '2-bosqich'), ('magistr', 'Magistratura'), ('para', 'Para sport')], default='1', max_length=10, verbose_name='Bosqich')),
                ('sport_turi_uz', models.CharField(max_length=200, verbose_name='Sport turi (Uz)')),
                ('sport_turi_ru', models.CharField(blank=True, max_length=200, verbose_name='Sport turi (Ru)')),
                ('sport_turi_en', models.CharField(blank=True, max_length=200, verbose_name='Sport turi (En)')),
                ('talabalar_soni', models.PositiveIntegerField(default=0, verbose_name='Talabalar soni')),
                ('jahon_chempionati_1', models.PositiveIntegerField(default=0)),
                ('jahon_chempionati_2', models.PositiveIntegerField(default=0)),
                ('jahon_chempionati_3', models.PositiveIntegerField(default=0)),
                ('para_osiyo_1', models.PositiveIntegerField(default=0)),
                ('para_osiyo_2', models.PositiveIntegerField(default=0)),
                ('para_osiyo_3', models.PositiveIntegerField(default=0)),
                ('osiyo_chempionati_1', models.PositiveIntegerField(default=0)),
                ('osiyo_chempionati_2', models.PositiveIntegerField(default=0)),
                ('osiyo_chempionati_3', models.PositiveIntegerField(default=0)),
                ('osiyo_kubogi_1', models.PositiveIntegerField(default=0)),
                ('osiyo_kubogi_2', models.PositiveIntegerField(default=0)),
                ('osiyo_kubogi_3', models.PositiveIntegerField(default=0)),
                ('xalqaro_turnir_1', models.PositiveIntegerField(default=0)),
                ('xalqaro_turnir_2', models.PositiveIntegerField(default=0)),
                ('xalqaro_turnir_3', models.PositiveIntegerField(default=0)),
                ('mdh_1', models.PositiveIntegerField(default=0)),
                ('mdh_2', models.PositiveIntegerField(default=0)),
                ('mdh_3', models.PositiveIntegerField(default=0)),
                ('osiyo_yoshlar_1', models.PositiveIntegerField(default=0)),
                ('osiyo_yoshlar_2', models.PositiveIntegerField(default=0)),
                ('osiyo_yoshlar_3', models.PositiveIntegerField(default=0)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
            ],
            options={
                'verbose_name': 'Sport natija qatori',
                'verbose_name_plural': 'Sport natijalari',
                'db_table': 'activities_sport_natija',
                'ordering': ['bosqich', 'order'],
            },
        ),
        migrations.CreateModel(
            name='SportKalendar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('yil', models.PositiveIntegerField(default=2026, verbose_name='Yil')),
                ('sport_turi_uz', models.CharField(max_length=200, verbose_name='Sport turi (Uz)')),
                ('sport_turi_ru', models.CharField(blank=True, max_length=200, verbose_name='Sport turi (Ru)')),
                ('sport_turi_en', models.CharField(blank=True, max_length=200, verbose_name='Sport turi (En)')),
                ('jahon_chempionati', models.PositiveIntegerField(default=0)),
                ('jahon_seriyasi', models.PositiveIntegerField(default=0)),
                ('jahon_kubogi', models.PositiveIntegerField(default=0)),
                ('yoshlar_olimpiya', models.PositiveIntegerField(default=0)),
                ('osiyo_oyinlari', models.PositiveIntegerField(default=0)),
                ('osiyo_chempionati', models.PositiveIntegerField(default=0)),
                ('osiyo_kubogi', models.PositiveIntegerField(default=0)),
                ('xalqaro_turnir', models.PositiveIntegerField(default=0)),
                ('ozb_chempionati', models.PositiveIntegerField(default=0)),
                ('ozb_kubogi', models.PositiveIntegerField(default=0)),
                ('prezident_olimpiyada', models.PositiveIntegerField(default=0)),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
            ],
            options={
                'verbose_name': 'Sport kalendari qatori',
                'verbose_name_plural': 'Sport kalendari',
                'db_table': 'activities_sport_kalendar',
                'ordering': ['-yil', 'order'],
            },
        ),
    ]
