"""
python manage.py seed_rektorat          # yaratadi / yangilaydi
python manage.py seed_rektorat --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.students.models import Person, PersonCategory, PersonContent
from common.models import Tag


# ── Taglar ────────────────────────────────────────────────────────────────────
TAGS = [
    # (slug, name_uz, name_ru, name_en)
    ("biografiya", "Biografiya", "Биография", "Biography"),
]


# ── Rahbariyat ma'lumotlari (PDF'dan verbatim) ────────────────────────────────
PERSONS = [
    # ═══════════════════════════════════════════════════════════════════════════
    # 1. Rektor
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 1,
        "is_head": True,
        "full_name_uz": "Tursunaliyev Ilhomjon Ahmedovich",
        "full_name_ru": "Турсуналиев Ильхомжон Ахмедович",
        "full_name_en": "Ilhomjon Ahmedovich Tursunaliyev",

        "title_uz": "Rektor",
        "title_ru": "Ректор",
        "title_en": "Rector",

        "position_uz": "",
        "position_ru": "",
        "position_en": "",

        # PDF sahifa 1 dan
        "address": "Toshkent shahri, Yashnobod tumani, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi",
        "reception": "Dushanba-shanba, 9:00-17:00",
        "phone": "+99877737971, +99877317972",
        "email": "info@usas.uz, akademiyasport@exat.uz",

        # PDF sahifa 1-3 dan — so'zma-so'z
        "bio_uz": (
            "Tursunaliyev Ilhomjon Ahmedovich 1971-yil 30-mayda Farg'ona viloyati Farg'ona tumanida "
            "tug'ilgan. 1996-yil Farg'ona davlat universitetini tamomlagan. "
            "1988–1993 yillarda bolalar va o'smirlar sport maktablarida o'qituvchi-murabbiy, "
            "1993–2015 yillarda turli lavozimlarda Farg'ona Olimpiya zaxiralari kollejida va "
            "texnikumlarda ishlagan. 2015–2022 yillarda Jismoniy tarbiya va sport bo'yicha "
            "mutaxassislarni qayta tayyorlash va malakasini oshirish markazi va instituti "
            "direktorligi lavozimida faoliyat yuritgan. 2022–2025 yillarda institut rektori, "
            "2025 yildan hozirgi kunga qadar O'zbekiston davlat sport akademiyasi rektori. "
            "Shu bilan birga \"Oliy ta'lim asoschisi\" ko'krak nishoniga ega."
        ),
        "bio_ru": (
            "Турсуналиев Ильхомжон Ахмедович родился 30 мая 1971 года в Ферганском районе "
            "Ферганской области. В 1996 году окончил Ферганский государственный университет. "
            "В 1988–1993 годах работал тренером и преподавателем-тренером в детских и юношеских "
            "спортивных школах, в 1993–2015 годах занимал различные должности в Ферганском колледже "
            "олимпийского резерва и техникумах. В 2015–2022 годах был директором Центра "
            "переподготовки и повышения квалификации специалистов по физической культуре и спорту, "
            "в 2022–2025 годах — ректором института, с 2025 года по настоящее время занимает "
            "должность ректора Государственной спортивной академии Узбекистана. "
            "Также награждён нагрудным знаком «Основатель высшего образования»."
        ),
        "bio_en": (
            "Ilhomjon Ahmedovich Tursunaliyev was born on May 30, 1971, in Fergana District, "
            "Fergana Region. He graduated from Fergana State University in 1996. "
            "From 1988 to 1993, he worked as a teacher-coach at children's and youth sports schools, "
            "and from 1993 to 2015, he held various positions at the Fergana Olympic Reserve College "
            "and technical schools. From 2015 to 2022, he served as Director of the Center for "
            "Retraining and Professional Development of Specialists in Physical Culture and Sports, "
            "and from 2022 to 2025, he was Rector of the Institute. Since 2025, he has been serving "
            "as Rector of the Uzbekistan State Sports Academy. He was also awarded the "
            "\"Founder of Higher Education\" badge."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. Birinchi Prorektor
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 2,
        "is_head": False,
        "full_name_uz": "Yusupov Zafarjon Zoirovich",
        "full_name_ru": "Юсупов Зафаржон Зоирович",
        "full_name_en": "Zafarjon Zoirovich Yusupov",

        # PDF sahifa 4 dan — aniq so'zlar bilan
        "title_uz": "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar birinchi prorektori",
        "title_ru": "Первый проректор по делам молодёжи и духовно-просветительской работе",
        "title_en": "First Vice-Rector for Youth Affairs and Spiritual-Educational Work",

        "position_uz": "",
        "position_ru": "",
        "position_en": "",

        "address": "Toshkent shahar Yashnobod tumani, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi",
        "reception": "Payshanba, 10:00-12:00",
        "phone": "+99877737971, +998777317972, +998777317973",
        "email": "info@usas.uz, akademiyasport@exat.uz",

        # PDF sahifa 4-7 dan — so'zma-so'z
        "bio_uz": (
            "Yusupov Zafarjon Zoirovich 1990-yil 16-may Toshkent shahrida tug'ilgan. "
            "2012-yil O\u02BBzbekiston Davlat jismoniy tarbiya institutining bakalavr bosqichini va "
            "2014-yil ayni institutning magistratura bosqichini tamomlagan. "
            "2014–2017 yillarda O'zbekiston davlat jismoniy tarbiya instituti \"Gandbol va tennis "
            "nazariyasi va uslubiyati\" kafedrasida o'qituvchi, 2017–2020 yillarda mazkur institut "
            "huzuridagi malaka oshirish markazi va institutida uslubchi va katta o'qituvchi, "
            "2018–2019 yillarda O'zbekiston Milliy Olimpiya qo'mitasi va sport federatsiyalarida "
            "yetakchi mutaxassis hamda bosh kotib, 2019–2025 yillarda O'zbekiston dzyudo "
            "federatsiyasida sport direktori, 2025 yilda Jismoniy tarbiya va sport bo'yicha "
            "mutaxassislarni qayta tayyorlash va malakasini oshirish institutida xalqaro aloqalar "
            "bo'limi boshlig'i lavozimlarida faoliyat yuritgan. Shu bilan birga 2019-yil "
            "\"Jismoniy tarbiya va sport a'lochisi\" ko'krak nishoniga ega. "
            "2025-yildan hozirgi kunga qadar O'zbekiston davlat sport akademiyasi yoshlar masalalari "
            "va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektori lavozimida faoliyat yuritib kelmoqda."
        ),
        "bio_ru": (
            "Юсупов Зафаржон Зоирович родился 16 мая 1990 года в городе Ташкенте. "
            "В 2012 году окончил бакалавриат, а в 2014 году магистратуру Узбекского "
            "государственного института физической культуры. "
            "В 2014–2017 годах работал преподавателем кафедры «Теория и методика гандбола и "
            "тенниса» Узбекского государственного института физической культуры, в 2017–2020 "
            "годах — методистом и старшим преподавателем в центре и институте повышения "
            "квалификации при данном учреждении. В 2018–2019 годах занимал должности ведущего "
            "специалиста и генерального секретаря в Национальном олимпийском комитете Узбекистана "
            "и спортивных федерациях, в 2019–2025 годах — спортивного директора Федерации дзюдо "
            "Узбекистана. В 2025 году работал начальником отдела международных связей Института "
            "переподготовки и повышения квалификации специалистов по физической культуре и спорту. "
            "Награждён нагрудным знаком «Отличник физической культуры и спорта» (2019 г.). "
            "С 2025 года по настоящее время занимает должность первого проректора по делам "
            "молодёжи и духовно-просветительской работе Государственной спортивной академии Узбекистана."
        ),
        "bio_en": (
            "Zafarjon Zoirovich Yusupov was born on May 16, 1990, in Tashkent. "
            "He graduated with a bachelor's degree in 2012 and a master's degree in 2014 from "
            "the Uzbekistan State Institute of Physical Culture. "
            "From 2014 to 2017, he worked as a lecturer at the Department of Theory and Methodology "
            "of Handball and Tennis at the same institute. Between 2017 and 2020, he served as a "
            "methodologist and senior lecturer at the center and institute for professional "
            "development under this institution. From 2018 to 2019, he held positions as a leading "
            "specialist and secretary general at the National Olympic Committee of Uzbekistan and "
            "sports federations. From 2019 to 2025, he was the sports director of the Judo "
            "Federation of Uzbekistan. In 2025, he worked as the head of the international relations "
            "department at the Institute for Retraining and Professional Development of Specialists "
            "in Physical Culture and Sports. He was awarded the \"Excellent Worker of Physical "
            "Culture and Sports\" badge (2019). Since 2025, he has been serving as the First "
            "Vice-Rector for Youth Affairs and Spiritual and Educational Work of the Uzbekistan "
            "State Sports Academy."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. O'quv ishlari bo'yicha prorektor
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 3,
        "is_head": False,
        "full_name_uz": "Ishtayev Dilshod Ravshanbekovich",
        "full_name_ru": "Иштаев Дилшод Равшанбекович",
        "full_name_en": "Dilshod Ravshanbekovich Ishtayev",

        "title_uz": "O'quv ishlari bo'yicha prorektor",
        "title_ru": "Проректор по учебной работе",
        "title_en": "Vice-Rector for Academic Affairs",

        "position_uz": "",
        "position_ru": "",
        "position_en": "",

        "address": "Toshkent shahri, Yashnobod tumani, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi",
        "reception": "Dushanba-shanba, 9:00-17:00",
        "phone": "+998977211465",
        "email": "info@usas.uz, akademiyasport@exat.uz",

        # PDF sahifa 8-11 dan — so'zma-so'z
        "bio_uz": (
            "Ishtayev Dilshod Ravshanbekovich 1979-yil 21-sentabrda Toshkent viloyati Bo'stonliq "
            "tumanida tug'ilgan. 2001-yil O'zbekiston Davlat Jismoniy tarbiya institutining bakalavr "
            "bosqichini va 2009-yil ayni institutning magistratura bosqichini tamomlagan. "
            "2001–2007 yillarda Toshkent viloyati Bo'stonliq tumanidagi 11-maktabda jismoniy tarbiya "
            "o'qituvchisi, 2009–2017 yillarda O'zbekiston davlat jismoniy tarbiya instituti "
            "\"Gimnastika nazariyasi va uslubiyati\" kafedrasida o'qituvchi va katta o'qituvchi, "
            "2017–2020 yillarda fakultet dekani vazifasini bajaruvchi va kafedra dotsenti, "
            "2020–2026 yillarda universitetning turli bo'limlari boshlig'i lavozimlarida "
            "faoliyat yuritgan. 2026 yildan hozirgi kunga qadar O'zbekiston davlat sport akademiyasi "
            "o'quv ishlari bo'yicha prorektori lavozimida ishlamoqda."
        ),
        "bio_ru": (
            "Иштаев Дилшод Равшанбекович родился 21 сентября 1979 года в Бостанлыкском районе "
            "Ташкентской области. В 2001 году окончил бакалавриат, а в 2009 году магистратуру "
            "Узбекского государственного института физической культуры. "
            "В 2001–2007 годах работал учителем физической культуры в 11-й школе Бостанлыкского "
            "района Ташкентской области, в 2009–2017 годах — преподавателем и старшим "
            "преподавателем кафедры «Теория и методика гимнастики» Узбекского государственного "
            "института физической культуры. В 2017–2020 годах занимал должности исполняющего "
            "обязанности декана факультета и доцента кафедры, в 2020–2026 годах — руководителя "
            "различных отделов университета. С 2026 года по настоящее время занимает должность "
            "проректора по учебной работе в Государственной спортивной академии Узбекистана."
        ),
        "bio_en": (
            "Dilshod Ravshanbekovich Ishtayev was born on September 21, 1979, in Bo'stonliq "
            "District, Tashkent Region. He graduated with a bachelor's degree in 2001 and a "
            "master's degree in 2009 from the Uzbekistan State Institute of Physical Culture. "
            "From 2001 to 2007, he worked as a physical education teacher at School No. 11 in "
            "Bo'stonliq District. From 2009 to 2017, he served as a lecturer and senior lecturer "
            "at the Department of \"Theory and Methodology of Gymnastics\" at the same institute. "
            "Between 2017 and 2020, he held positions as acting dean of the faculty and department "
            "associate professor, and from 2020 to 2026, he led various university departments. "
            "Since 2026, he has been serving as Vice-Rector for Academic Affairs at the Uzbekistan "
            "State Sports Academy."
        ),
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. Ilmiy ishlar va innovatsiyalar bo'yicha prorektor
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 4,
        "is_head": False,
        "full_name_uz": "Rasulov Zokir Pardayevich",
        "full_name_ru": "Расулов Зокир Пардаевич",
        "full_name_en": "Zokir Pardayevich Rasulov",

        "title_uz": "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
        "title_ru": "Проректор по научной работе и инновациям",
        "title_en": "Vice-Rector for Research and Innovation",

        "position_uz": "Dotsent",
        "position_ru": "Доцент",
        "position_en": "Associate Professor",

        "address": "Toshkent shahri, Yashnobod tumani, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi",
        "reception": "Dushanba-shanba, 9:00-17:00",
        "phone": "+998777317973",
        "email": "info@usas.uz, akademiyasport@exat.uz",

        # PDF sahifa 12-16 dan — to'liq, so'zma-so'z
        # NOTE: oldingi versiyada 2018-2022 yillar qismi tushib qolgan edi
        "bio_uz": (
            "Rasulov Zokir Pardayevich 1984-yil 24-iyunda Surxandaryo viloyati Denov tumanida "
            "tug'ilgan. 2006-yil Qarshi Davlat universitetini bakalavr bosqichini va 2008-yil "
            "O'zbekiston Milliy universitetining magistratura bosqichini tamomlagan. "
            "2006–2008-yillarda Toshkent pedagogika kollejida o'qituvchi va tarbiyachi, "
            "2008–2012-yillarda Toshkent davlat iqtisodiyot universitetida pedagogika va iqtisodiy "
            "pedagogika kafedrasida assistent va kichik ilmiy xodim. "
            "2012–2018-yillarda O'zbekiston davlat jismoniy tarbiya va sport universitetining ichki "
            "nazorat va monitoring bo'limi boshlig'i, 2018–2022-yillarda Jismoniy tarbiya va sport "
            "bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish markazi va institutida "
            "yuqori rahbarlik lavozimlarida faoliyat yuritgan, jumladan, ilmiy-metodik ishlarga "
            "mas'ul prorektor va ilmiy ishlar va xalqaro aloqalar bo'yicha prorektor, direktor "
            "o'rinbosari lavozimlarida ishlagan. "
            "2025-yildan hozirgi kunga qadar O'zbekiston davlat sport akademiyasi ilmiy ishlar "
            "va innovatsiyalar bo'yicha prorektori lavozimida faoliyat yuritib kelmoqda."
        ),
        "bio_ru": (
            "Расулов Зокир Пардаевич родился 24 июня 1984 года в Деновском районе "
            "Сурхандарьинской области. В 2006 году окончил бакалавриат Каршского государственного "
            "университета, а в 2008 году магистратуру Национального университета Узбекистана. "
            "В 2006–2008 годах работал преподавателем и воспитателем в Ташкентском педагогическом "
            "колледже, в 2008–2012 годах — ассистентом и младшим научным сотрудником на кафедре "
            "педагогики и экономической педагогики Ташкентского государственного университета "
            "экономики. В 2012–2018 годах был руководителем отдела внутреннего контроля и "
            "мониторинга Узбекского государственного университета физической культуры и спорта, "
            "в 2018–2022 годах занимал руководящие должности в Центре и Институте переподготовки "
            "и повышения квалификации специалистов по физической культуре и спорту, включая "
            "проректора по научно-методической работе и проректора по научной работе и "
            "международным связям. Имеет учёное звание доцента. С 2025 года по настоящее время "
            "занимает должность проректора по научной работе и инновациям в Государственной "
            "спортивной академии Узбекистана."
        ),
        "bio_en": (
            "Zokir Pardayevich Rasulov was born on June 24, 1984, in Denov District, "
            "Surkhandarya Region. He graduated with a bachelor's degree from Qarshi State "
            "University in 2006 and a master's degree from the National University of Uzbekistan "
            "in 2008. From 2006 to 2008, he worked as a teacher and tutor at the Tashkent "
            "Pedagogical College, and from 2008 to 2012, he served as an assistant and junior "
            "researcher at the Department of Pedagogy and Economic Pedagogy at Tashkent State "
            "University of Economics. Between 2012 and 2018, he was Head of the Internal Control "
            "and Monitoring Department at the Uzbekistan State University of Physical Culture and "
            "Sports. From 2018 to 2022, he held senior leadership positions at the Center and "
            "Institute for Retraining and Professional Development of Specialists in Physical "
            "Culture and Sports, including Vice-Rector for Scientific and Methodological Work and "
            "Vice-Rector for Research and International Relations. He holds the academic title of "
            "Associate Professor. Since 2025, he has been serving as Vice-Rector for Research and "
            "Innovation at the Uzbekistan State Sports Academy."
        ),
    },
]


class Command(BaseCommand):
    help = "Rektorat a'zolarini Person jadvaliga to'ldiradi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help="Rektorat kategoriyasidagi barcha yozuvlarni o'chirib, qaytadan yozadi",
        )

    def handle(self, *args, **options):
        # ── 1. PersonCategory — Rektorat ────────────────────────────────────
        cat, cat_created = PersonCategory.objects.update_or_create(
            slug='rektorat',
            defaults={
                'title_uz': 'Rektorat',
                'title_ru': 'Ректорат',
                'title_en': 'Rectorate',
                'order': 1,
            },
        )
        self.stdout.write(
            f"  [kat] {'yaratildi' if cat_created else 'yangilandi'}: {cat.title_uz}"
        )

        # ── 2. Tag — Biografiya ─────────────────────────────────────────────
        tag_map = {}
        for slug, name_uz, name_ru, name_en in TAGS:
            tag, tag_created = Tag.objects.update_or_create(
                slug=slug,
                defaults={
                    'name_uz': name_uz,
                    'name_ru': name_ru,
                    'name_en': name_en,
                },
            )
            tag_map[slug] = tag
            self.stdout.write(
                f"  [tag] {'yaratildi' if tag_created else 'yangilandi'}: {tag.name_uz}"
            )

        bio_tag = tag_map['biografiya']

        # ── 3. Clear (ixtiyoriy) ────────────────────────────────────────────
        if options['clear']:
            persons_qs = Person.objects.filter(category=cat)
            for p in persons_qs:
                p.tabs.all().delete()
            deleted = persons_qs.delete()[0]
            self.stdout.write(self.style.WARNING(
                f"  O'chirildi: {deleted} ta shaxs (Rektorat)"
            ))

        # ── 4. Person + PersonContent ───────────────────────────────────────
        created_n = updated_n = 0
        for data in PERSONS:
            person, is_new = Person.objects.update_or_create(
                full_name_uz=data['full_name_uz'],
                category=cat,
                defaults={
                    'full_name_ru': data['full_name_ru'],
                    'full_name_en': data['full_name_en'],
                    'title_uz':     data['title_uz'],
                    'title_ru':     data['title_ru'],
                    'title_en':     data['title_en'],
                    'position_uz':  data['position_uz'],
                    'position_ru':  data['position_ru'],
                    'position_en':  data['position_en'],
                    'phone':        data['phone'],
                    'email':        data['email'],
                    'address':      data['address'],
                    'reception':    data['reception'],
                    'is_head':      data['is_head'],
                    'is_active':    True,
                    'order':        data['order'],
                },
            )

            # Biografiya tab
            tab, _ = PersonContent.objects.update_or_create(
                person=person,
                order=1,
                defaults={
                    'content_uz': data['bio_uz'],
                    'content_ru': data['bio_ru'],
                    'content_en': data['bio_en'],
                },
            )
            if not tab.tags.filter(pk=bio_tag.pk).exists():
                tab.tags.add(bio_tag)

            if is_new:
                created_n += 1
            else:
                updated_n += 1

            self.stdout.write(
                f"  {'[+]' if is_new else '[~]'} {data['full_name_uz']} — {data['title_uz']}"
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created_n} yangi, {updated_n} yangilandi. "
            f"Jami {len(PERSONS)} ta rektorat a'zosi."
        ))
