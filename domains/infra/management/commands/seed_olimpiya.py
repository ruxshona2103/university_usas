"""
python manage.py seed_olimpiya          # yaratadi / yangilaydi
python manage.py seed_olimpiya --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.infra.models import OlimpiyaShaharchasi, OlimpiyaGalleryImage


INTRO_UZ = """
<ul>
  <li>Qurilish maydoni — 7.1 gektar</li>
  <li>Kukalamzorlashtirish — 47.5 gektar</li>
  <li>47.5 gektar maydonga bog'lar, suv havzalari, yugurish yo'laklari va ochiq sport maydonlari barpo etiladi</li>
  <li>Asosiy kirish darvozalari — 12 ta (piyodalar uchun 6 ta, avtomobillarga 6 ta)</li>
  <li>1 900 o'rinli avtoturargoh mavjud</li>
</ul>

<h2>15 ta ochiq maydon</h2>
<ul>
  <li>1 ta 68x105 o'lchamli yengil atletika va futbol maydoni</li>
  <li>2 ta 65x106 o'lchamli chim ustida xokkey maydoni</li>
  <li>2 ta 20x40 o'lchamli mini-futbol maydoni</li>
  <li>4 ta 10,97x23,77 o'lchamli tennis korti</li>
  <li>2 ta 8x16 o'lchamli sohil voleyboli maydoni</li>
  <li>2 ta 11x15 o'lchamli 3x3 basketbol maydoni</li>
</ul>

<h2>206x68 maydonda</h2>
<ul>
  <li>1 ta 300 metrlik trassa — BMX maydoni</li>
  <li>1 ta skeytbord maydoni</li>
</ul>

<h2>Barpo etilayotgan bino-inshootlar</h2>
<ul>
  <li>3 qavatli Davlat sport-tibbiyoti ilmiy-amaliy markazi</li>
  <li>5 qavatli 400 o'rinli Paralimpiya terma jamoalari yotoqxonasi</li>
  <li>21 km uzunlikdagi Yangi O'zbekiston bog'i va Olimpiya shaharchasi hududidan o'tuvchi yugurish va velosport yo'lagi</li>
</ul>
""".strip()


INTRO_RU = """
<p><strong>Олимпийский городок</strong> — один из крупнейших объектов спортивной инфраструктуры Узбекистана.</p>

<h2>Общие показатели</h2>
<ul>
  <li>Общая площадь — <strong>100,4 гектара</strong></li>
  <li>Площадь застройки — <strong>7,1 гектара</strong></li>
  <li>Озеленение — <strong>47,5 гектара</strong></li>
  <li>На площади 47,5 гектара будут разбиты парки, водоёмы, беговые дорожки и открытые спортивные площадки</li>
  <li>Главных въездных ворот — <strong>12</strong> (6 для пешеходов, 6 для автомобилей)</li>
  <li>Автостоянка на <strong>1 900 мест</strong></li>
</ul>

<h2>15 открытых площадок</h2>
<ul>
  <li>1 поле <strong>68×105</strong> м — лёгкая атлетика и футбол</li>
  <li>2 поля <strong>65×106</strong> м — хоккей на траве</li>
  <li>2 поля <strong>20×40</strong> м — мини-футбол</li>
  <li>4 корта <strong>10,97×23,77</strong> м — теннис</li>
  <li>2 площадки <strong>8×16</strong> м — пляжный волейбол</li>
  <li>2 площадки <strong>11×15</strong> м — баскетбол 3×3</li>
</ul>

<h2>На площадке 206×68 м</h2>
<ul>
  <li>1 трасса длиной <strong>300 метров</strong> — BMX</li>
  <li>1 площадка для скейтборда</li>
</ul>

<h2>Строящиеся объекты</h2>
<ul>
  <li>3-этажный <strong>Государственный научно-практический центр спортивной медицины</strong></li>
  <li>5-этажное общежитие паралимпийских сборных на <strong>400 мест</strong></li>
  <li>Беговая и велосипедная дорожка протяжённостью <strong>21 км</strong> через парк «Новый Узбекистан» и территорию Олимпийского городка</li>
</ul>
""".strip()


INTRO_EN = """
<p><strong>Olympic Village</strong> is one of the largest sports infrastructure facilities in Uzbekistan.</p>

<h2>General figures</h2>
<ul>
  <li>Total area — <strong>100.4 hectares</strong></li>
  <li>Construction area — <strong>7.1 hectares</strong></li>
  <li>Green area — <strong>47.5 hectares</strong></li>
  <li>47.5 hectares will feature parks, water reservoirs, running tracks and open sports grounds</li>
  <li>Main entrance gates — <strong>12</strong> (6 for pedestrians, 6 for vehicles)</li>
  <li>Parking lot with <strong>1,900 spaces</strong></li>
</ul>

<h2>15 open sports areas</h2>
<ul>
  <li>1 field <strong>68×105 m</strong> — athletics and football</li>
  <li>2 fields <strong>65×106 m</strong> — field hockey</li>
  <li>2 fields <strong>20×40 m</strong> — mini-football</li>
  <li>4 courts <strong>10.97×23.77 m</strong> — tennis</li>
  <li>2 courts <strong>8×16 m</strong> — beach volleyball</li>
  <li>2 courts <strong>11×15 m</strong> — 3×3 basketball</li>
</ul>

<h2>206×68 m zone</h2>
<ul>
  <li>1 track <strong>300 metres</strong> long — BMX</li>
  <li>1 skateboard park</li>
</ul>

<h2>Facilities under construction</h2>
<ul>
  <li>3-storey <strong>State Sports Medicine Research and Practice Centre</strong></li>
  <li>5-storey dormitory for Paralympic national teams — <strong>400 beds</strong></li>
  <li><strong>21 km</strong> running and cycling path through New Uzbekistan Park and the Olympic Village</li>
</ul>
""".strip()


class Command(BaseCommand):
    help = "Olimpiya shaharchasi uchun boshlang'ich ma'lumotlarni yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Mavjud ma'lumotlarni o'chirib, qaytadan yozadi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            OlimpiyaShaharchasi.objects.all().delete()
            self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        obj = OlimpiyaShaharchasi.objects.first()
        if obj is None:
            OlimpiyaShaharchasi.objects.create(
                intro_uz=INTRO_UZ,
                intro_ru=INTRO_RU,
                intro_en=INTRO_EN,
                gallery_title_uz='Fotogaleriya',
                gallery_title_ru='Фотогалерея',
                gallery_title_en='Photo gallery',
            )
            self.stdout.write(self.style.SUCCESS("Olimpiya shaharchasi ma'lumotlari yaratildi."))
        else:
            obj.intro_uz = INTRO_UZ
            obj.intro_ru = INTRO_RU
            obj.intro_en = INTRO_EN
            obj.gallery_title_uz = 'Fotogaleriya'
            obj.gallery_title_ru = 'Фотогалерея'
            obj.gallery_title_en = 'Photo gallery'
            obj.save()
            self.stdout.write(self.style.SUCCESS("Olimpiya shaharchasi ma'lumotlari yangilandi."))

        self.stdout.write(self.style.NOTICE(
            "Rasmlar qo'shish uchun admin panelga kiring: /admin/ > Olimpiya shaharchasi"
        ))
