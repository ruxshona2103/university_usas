from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.activities.models import (
    ContractPrice,
    ServiceVehicle,
    IlmiyFaoliyat,
    IlmiyFaoliyatCategory,
    IlmiyYonalish,
    IlmiyYonalishItem,
    SportStat,
    SportYonalish,
    SportTadbir,
    AxborotVazifa,
    AxborotXodim,
)


def _safe_file_url(field, request=None):
    """
    Return a robust absolute URL for FileField values.
    - Already-absolute URLs (ImageKit CDN) → as-is
    - Relative /media/... paths → prepend scheme+host via request
    """
    if not field:
        return None

    name = (getattr(field, 'name', '') or '').strip()
    if not name:
        return None

    # Already absolute (ImageKit, S3, etc.)
    if name.startswith(('http://', 'https://')):
        return name

    try:
        url = field.url
    except Exception:
        url = name

    # url is relative like /media/... — build absolute from root, not current path
    if request and not str(url).startswith(('http://', 'https://')):
        # build_absolute_uri('/media/...') always works correctly with leading slash
        if not url.startswith('/'):
            url = '/' + url
        return request.build_absolute_uri(url)
    return url


_EDUCATION_TYPE_LABELS = {
    'bachelor': {'uz': 'Bakalavr',     'ru': 'Бакалавриат',  'en': 'Bachelor'},
    'master':   {'uz': 'Magistratura', 'ru': 'Магистратура', 'en': 'Master'},
}

_EDUCATION_FORM_LABELS = {
    'daytime':  {'uz': 'Kunduzgi', 'ru': 'Дневная',  'en': 'Daytime'},
    'evening':  {'uz': 'Kechki',   'ru': 'Вечерняя', 'en': 'Evening'},
    'distance': {'uz': 'Sirtqi',   'ru': 'Заочная',  'en': 'Distance'},
}


class ContractPriceSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    education_type = serializers.SerializerMethodField()
    education_form = serializers.SerializerMethodField()

    class Meta:
        model  = ContractPrice
        fields = [
            'id', 'specialty_code', 'specialty_name',
            'education_type', 'education_form',
            'price', 'order',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_specialty_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'specialty_name_{lang}') or obj.specialty_name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_education_type(self, obj):
        lang = self.context.get('lang', 'uz')
        return _EDUCATION_TYPE_LABELS.get(obj.education_type, {}).get(lang) or obj.get_education_type_display()

    @extend_schema_field(OpenApiTypes.STR)
    def get_education_form(self, obj):
        lang = self.context.get('lang', 'uz')
        return _EDUCATION_FORM_LABELS.get(obj.education_form, {}).get(lang) or obj.get_education_form_display()


class ServiceVehicleSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.SerializerMethodField()
    fuel_type    = serializers.CharField(source='get_fuel_type_display')

    class Meta:
        model  = ServiceVehicle
        fields = [
            'id', 'name', 'vehicle_type',
            'manufactured_year', 'fuel_type', 'order',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_vehicle_type(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'vehicle_type_{lang}') or obj.vehicle_type_uz


class IlmiyFaoliyatSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    file_url    = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'description', 'image_url', 'file_url', 'order', 'is_active', 'created_at', 'updated_at']

    def _req(self):
        return self.context.get('request')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_image_url(self, obj):
        req = self._req()
        uz = _safe_file_url(obj.image, req)
        return {'uz': uz, 'ru': _safe_file_url(obj.image_ru, req) or uz, 'en': _safe_file_url(obj.image_en, req) or uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_file_url(self, obj):
        return _safe_file_url(obj.file, self._req())


class IlmiyFaoliyatItemSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    file_url    = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'description', 'image_url', 'file_url', 'order', 'is_active']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'description_{lang}') or obj.description_uz or ''

    def get_image_url(self, obj):
        req = self.context.get('request')
        lang = self.context.get('lang', 'uz')
        field = getattr(obj, f'image_{lang}', None) if lang != 'uz' else None
        return _safe_file_url(field, req) or _safe_file_url(obj.image, req)

    def get_file_url(self, obj):
        return _safe_file_url(obj.file, self.context.get('request'))


class IlmiyFaoliyatSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'order', 'items']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_items(self, obj):
        # prefetch_related cache dan oladi — .filter() ishlatmaymiz
        qs = obj.items.all()
        return IlmiyFaoliyatItemSerializer(qs, many=True, context=self.context).data


class IlmiyFaoliyatCategoryTreeSerializer(serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    items         = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'order', 'subcategories', 'items']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_subcategories(self, obj):
        # prefetch cache dan oladi
        return IlmiyFaoliyatSubCategorySerializer(obj.children.all(), many=True, context=self.context).data

    def get_items(self, obj):
        # prefetch cache dan oladi
        return IlmiyFaoliyatItemSerializer(obj.items.all(), many=True, context=self.context).data


class IlmiyFaoliyatCategorySimpleSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'description', 'icon', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}


class FaoliyatSubcategoryWriteSerializer(serializers.ModelSerializer):
    """Subcategory yaratish/yangilash uchun."""

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = [
            'id', 'parent',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'icon', 'order',
        ]
        read_only_fields = ['id']


class IlmiyFaoliyatWriteSerializer(serializers.ModelSerializer):
    """IlmiyFaoliyat item yaratish/yangilash uchun."""

    class Meta:
        model  = IlmiyFaoliyat
        fields = [
            'id', 'category',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'image', 'file', 'order', 'is_active',
        ]
        read_only_fields = ['id']


class IlmiyFaoliyatCategorySerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    blocks      = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'description', 'order', 'blocks']

    def _item_url(self, item):
        return _safe_file_url(item.file, self.context.get('request'))

    def _item_to_link(self, item):
        req = self.context.get('request')
        return {
            'id':          str(item.id),
            'label':       {'uz': item.title_uz or '', 'ru': item.title_ru or '', 'en': item.title_en or ''},
            'description': {'uz': item.description_uz or '', 'ru': item.description_ru or '', 'en': item.description_en or ''},
            'image_url':   _safe_file_url(item.image, req),
            'file_url':    _safe_file_url(item.file, req),
            'order':       item.order,
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(serializers.ListField())
    def get_blocks(self, obj):
        result = []

        # Sub-kategoriyalar → har biri structure-links blok (prefetch cache)
        for cat in obj.children.all():
            links = [self._item_to_link(item) for item in cat.items.all()]
            result.append({
                'type': 'structure-links',
                'data': {
                    'title': {'uz': cat.title_uz or '', 'ru': cat.title_ru or '', 'en': cat.title_en or ''},
                    'links': links,
                },
            })

        # To'g'ridan-to'g'ri itemlar → title bo'yicha guruhlash → har bir guruh bitta blok
        groups: dict = {}
        for item in obj.items.all():
            key = (item.title_uz or '', item.title_ru or '', item.title_en or '')
            if key not in groups:
                groups[key] = {
                    'title': {'uz': item.title_uz or '', 'ru': item.title_ru or '', 'en': item.title_en or ''},
                    'links': [],
                }
            groups[key]['links'].append(self._item_to_link(item))

        for group in groups.values():
            result.append({'type': 'structure-links', 'data': group})

        return result


# ──────────────────────────── Sport Faoliyat sahifasi ────────────────────────────

class SportStatSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = SportStat
        fields = ['id', 'value', 'suffix', 'title', 'color', 'order', 'created_at', 'updated_at']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz


class SportStatWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SportStat
        fields = ['id', 'title_uz', 'title_ru', 'title_en', 'value', 'suffix', 'color', 'order', 'is_active']
        read_only_fields = ['id']


class SportYonalishSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = SportYonalish
        fields = ['id', 'icon', 'title', 'description', 'order', 'created_at', 'updated_at']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'description_{lang}') or obj.description_uz or ''


class SportYonalishWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SportYonalish
        fields = [
            'id', 'icon',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'order', 'is_active',
        ]
        read_only_fields = ['id']


class SportTadbirSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    location    = serializers.SerializerMethodField()

    class Meta:
        model  = SportTadbir
        fields = ['id', 'title', 'description', 'location', 'event_date', 'order', 'created_at', 'updated_at']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'description_{lang}') or obj.description_uz or ''

    def get_location(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'location_{lang}') or obj.location_uz or ''


class SportTadbirWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SportTadbir
        fields = [
            'id',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'location_uz', 'location_ru', 'location_en',
            'event_date', 'order', 'is_active',
        ]
        read_only_fields = ['id']


# ──────────────────────────── Axborot xizmati ────────────────────────────

class AxborotVazifaSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = AxborotVazifa
        fields = ['id', 'title', 'order']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz


class AxborotVazifaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AxborotVazifa
        fields = ['id', 'title_uz', 'title_ru', 'title_en', 'order', 'is_active']
        read_only_fields = ['id']


class AxborotXodimSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model  = AxborotXodim
        fields = ['id', 'full_name', 'position', 'phone', 'email', 'photo_url', 'order', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'full_name_{lang}') or obj.full_name_uz

    def get_position(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'position_{lang}') or obj.position_uz

    def get_photo_url(self, obj):
        return _safe_file_url(obj.photo, self.context.get('request'))


class AxborotXodimWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AxborotXodim
        fields = [
            'id',
            'full_name_uz', 'full_name_ru', 'full_name_en',
            'position_uz', 'position_ru', 'position_en',
            'phone', 'email', 'photo', 'order', 'is_active',
        ]
        read_only_fields = ['id']


# ── Ilmiy yo'nalish (yangi sodda model) ──────────────────────────────────────

class IlmiyYonalishListSerializer(serializers.ModelSerializer):
    """Parent ro'yxati uchun — faqat name + slug."""
    name = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyYonalish
        fields = ['id', 'name', 'slug', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', None) or obj.name_uz


class IlmiyYonalishItemSerializer(serializers.ModelSerializer):
    """Child element — name, description, photo, slug."""
    name        = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo       = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyYonalishItem
        fields = ['id', 'name', 'description', 'photo', 'slug', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', None) or obj.name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}', None) or obj.description_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_photo(self, obj):
        return _safe_file_url(obj.photo, self.context.get('request'))


class IlmiyYonalishDetailSerializer(serializers.ModelSerializer):
    """Parent + ichidagi child elementlar bilan."""
    name  = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyYonalish
        fields = ['id', 'name', 'slug', 'order', 'items']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', None) or obj.name_uz

    @extend_schema_field(IlmiyYonalishItemSerializer(many=True))
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order', 'name_uz')
        return IlmiyYonalishItemSerializer(qs, many=True, context=self.context).data


# ── Ilmiy kontent (jurnallar, kengash, loyihalar, maktablar) ────────────────

from domains.activities.models import (
    IlmiyKontentSahifa, IlmiyJurnal, IlmiyKengashSeminar,
    IlmiyLoyiha, IlmiyMaktab, IlmiyAnjuman,
)


def _local(obj, field, lang):
    return getattr(obj, f"{field}_{lang}", None) or getattr(obj, f"{field}_uz", "") or ""


class IlmiyKontentSahifaSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    intro = serializers.SerializerMethodField()

    class Meta:
        model = IlmiyKontentSahifa
        fields = ['kategoriya', 'title', 'intro']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        return _local(obj, 'title', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_intro(self, obj):
        return _local(obj, 'intro', self._lang())


class IlmiyJurnalSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = IlmiyJurnal
        fields = ['id', 'name', 'description', 'image_url', 'link', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        return _local(obj, 'name', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        return _local(obj, 'description', self._lang())

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_image_url(self, obj):
        req = self.context.get('request')
        uz = _safe_file_url(obj.image, req)
        return {'uz': uz, 'ru': _safe_file_url(obj.image_ru, req) or uz, 'en': _safe_file_url(obj.image_en, req) or uz}


class IlmiyKengashSeminarSerializer(serializers.ModelSerializer):
    ixtisoslik_nomi = serializers.SerializerMethodField()
    rais = serializers.SerializerMethodField()
    rais_lavozim = serializers.SerializerMethodField()
    kotib = serializers.SerializerMethodField()
    kotib_lavozim = serializers.SerializerMethodField()

    class Meta:
        model = IlmiyKengashSeminar
        fields = [
            'id', 'tipi', 'shifr', 'buyruq_sanasi', 'ixtisoslik_shifri',
            'ixtisoslik_nomi', 'rais', 'rais_lavozim',
            'kotib', 'kotib_lavozim', 'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_ixtisoslik_nomi(self, obj):
        return _local(obj, 'ixtisoslik_nomi', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_rais(self, obj):
        return _local(obj, 'rais', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_rais_lavozim(self, obj):
        return _local(obj, 'rais_lavozim', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_kotib(self, obj):
        return _local(obj, 'kotib', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_kotib_lavozim(self, obj):
        return _local(obj, 'kotib_lavozim', self._lang())


class IlmiyLoyihaSerializer(serializers.ModelSerializer):
    raqami = serializers.SerializerMethodField()
    mavzusi = serializers.SerializerMethodField()

    class Meta:
        model = IlmiyLoyiha
        fields = ['id', 'raqami', 'mavzusi', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_raqami(self, obj):
        return _local(obj, 'raqami', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_mavzusi(self, obj):
        return _local(obj, 'mavzusi', self._lang())


class IlmiyMaktabSerializer(serializers.ModelSerializer):
    nomi = serializers.SerializerMethodField()
    asoschi = serializers.SerializerMethodField()

    class Meta:
        model = IlmiyMaktab
        fields = ['id', 'nomi', 'asoschi', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_nomi(self, obj):
        return _local(obj, 'nomi', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_asoschi(self, obj):
        return _local(obj, 'asoschi', self._lang())


class IlmiyAnjumanSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    location    = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    type        = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyAnjuman
        fields = ['id', 'title', 'description', 'date', 'location',
                  'type', 'status', 'image_url', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        return _local(obj, 'title', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        return _local(obj, 'description', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_location(self, obj):
        return _local(obj, 'location', self._lang())

    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, obj):
        return obj.turi


# ── Sport natijalari va kalendar ─────────────────────────────────────────────

from domains.activities.models import SportNatija, SportKalendar


class SportNatijaSerializer(serializers.ModelSerializer):
    sport_turi = serializers.SerializerMethodField()
    bosqich_display = serializers.CharField(source='get_bosqich_display', read_only=True)
    jami = serializers.IntegerField(read_only=True)

    class Meta:
        model = SportNatija
        fields = [
            'id', 'bosqich', 'bosqich_display', 'sport_turi', 'talabalar_soni',
            'jahon_chempionati_1', 'jahon_chempionati_2', 'jahon_chempionati_3',
            'jahon_kubogi_1', 'jahon_kubogi_2', 'jahon_kubogi_3',
            'para_osiyo_1', 'para_osiyo_2', 'para_osiyo_3',
            'osiyo_chempionati_1', 'osiyo_chempionati_2', 'osiyo_chempionati_3',
            'osiyo_kubogi_1', 'osiyo_kubogi_2', 'osiyo_kubogi_3',
            'xalqaro_turnir_1', 'xalqaro_turnir_2', 'xalqaro_turnir_3',
            'prezident_1', 'prezident_2', 'prezident_3',
            'ozb_chempionati_1', 'ozb_chempionati_2', 'ozb_chempionati_3',
            'ozb_kubogi_1', 'ozb_kubogi_2', 'ozb_kubogi_3',
            'jami', 'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_sport_turi(self, obj):
        lang = self._lang()
        return getattr(obj, f'sport_turi_{lang}') or obj.sport_turi_uz


class SportKalendarSerializer(serializers.ModelSerializer):
    sport_turi = serializers.SerializerMethodField()
    jami = serializers.IntegerField(read_only=True)

    class Meta:
        model = SportKalendar
        fields = [
            'id', 'yil', 'sport_turi',
            'jahon_chempionati', 'jahon_seriyasi', 'jahon_kubogi',
            'yoshlar_olimpiya', 'osiyo_oyinlari', 'osiyo_chempionati',
            'osiyo_kubogi', 'xalqaro_turnir',
            'ozb_chempionati', 'ozb_kubogi', 'prezident_olimpiyada',
            'jami', 'order',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_sport_turi(self, obj):
        lang = self._lang()
        return getattr(obj, f'sport_turi_{lang}') or obj.sport_turi_uz
