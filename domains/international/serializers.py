from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.international.models import (
    ForeignProfessorReview, PartnerOrganization, PartnerPageConfig,
    InternationalPost, InternationalPostImage,
    InternationalRating, InternationalRatingImage,
    NationalRating, NationalRatingImage,
    InternationalDeptConfig, MemorandumStat,
    AkademikAlmashinuv, AkademikAlmashinuvRasm,
    XalqaroReytingBolim, XalqaroReytingBolimRasm,
    XorijlikProfessor,
    StudyInUzbekistanConfig,
)


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class ForeignProfessorReviewSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    review   = serializers.SerializerMethodField()
    photo    = serializers.SerializerMethodField()

    class Meta:
        model  = ForeignProfessorReview
        fields = ['id', 'full_name', 'position', 'country', 'photo', 'review', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_review(self, obj):
        lang = self._lang()
        return getattr(obj, f'review_{lang}') or obj.review_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_photo(self, obj):
        return _abs_url(self.context.get('request'), obj.photo)


class PartnerOrganizationSerializer(serializers.ModelSerializer):
    title   = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    logo    = serializers.SerializerMethodField()
    image   = serializers.SerializerMethodField()

    class Meta:
        model  = PartnerOrganization
        fields = ['id', 'partner_type', 'title', 'country', 'logo', 'image', 'website', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_country(self, obj):
        lang = self._lang()
        return getattr(obj, f'country_{lang}') or obj.country_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_logo(self, obj):
        return _abs_url(self.context.get('request'), obj.logo)

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class PartnerPageConfigSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = PartnerPageConfig
        fields = ['title', 'description']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}


class InternationalDeptConfigSerializer(serializers.ModelSerializer):
    head_name          = serializers.SerializerMethodField()
    head_position      = serializers.SerializerMethodField()
    head_working_hours = serializers.SerializerMethodField()
    tasks              = serializers.SerializerMethodField()
    digital_data       = serializers.SerializerMethodField()
    head_photo         = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalDeptConfig
        fields = [
            'slug',
            'head_name', 'head_position', 'head_working_hours',
            'head_phone', 'head_email', 'head_photo', 'tasks',
            'digital_data',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_head_name(self, obj):
        return getattr(obj, f'head_name_{self._lang()}') or obj.head_name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_head_position(self, obj):
        return getattr(obj, f'head_position_{self._lang()}') or obj.head_position_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_head_working_hours(self, obj):
        return getattr(obj, f'head_working_hours_{self._lang()}') or obj.head_working_hours_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_head_photo(self, obj):
        return _abs_url(self.context.get('request'), obj.head_photo)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_tasks(self, obj):
        raw = getattr(obj, f'tasks_{self._lang()}') or obj.tasks_uz or ''
        tasks = []
        for line in raw.splitlines():
            s = line.strip()
            if not s:
                continue
            # "RAQAMLI MA'LUMOTLAR" sarlavhasidan keyingi qatorlar alohida
            # `memorandum_stats` bo'limiga o'tadi — vazifalar ro'yxatiga kirmaydi.
            if 'raqamli ma' in s.lower():
                break
            tasks.append(s)
        return tasks

    @extend_schema_field(OpenApiTypes.STR)
    def get_digital_data(self, obj):
        return (getattr(obj, f'digital_data_{self._lang()}') or obj.digital_data_uz or '').strip()


class MemorandumStatSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model  = MemorandumStat
        fields = ['id', 'organization', 'foreign_count', 'domestic_count', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_organization(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'organization_{lang}') or obj.organization_uz


class InternationalPostImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalPostImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InternationalRatingImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalRatingImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class NationalRatingImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    class Meta:
        model = NationalRatingImage
        fields = ['id', 'image', 'alt', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        lang = self.context.get('lang', 'uz')
        img = getattr(obj, f'image_{lang}', None) or obj.image_uz
        return _abs_url(self.context.get('request'), img)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_alt(self, obj):
        return {
            'uz': obj.alt_uz or '',
            'ru': obj.alt_ru or obj.alt_uz or '',
            'en': obj.alt_en or obj.alt_uz or '',
        }


class InternationalRatingSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cover       = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalRating
        fields = ['id', 'slug', 'title', 'description', 'cover', 'images', 'date', 'order', 'created_at', 'updated_at']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {
            'uz': obj.title_uz or '',
            'ru': obj.title_ru or obj.title_uz or '',
            'en': obj.title_en or obj.title_uz or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {
            'uz': obj.description_uz or '',
            'ru': obj.description_ru or obj.description_uz or '',
            'en': obj.description_en or obj.description_uz or '',
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_cover(self, obj):
        return _abs_url(self.context.get('request'), obj.cover)

    @extend_schema_field(InternationalRatingImageSerializer(many=True))
    def get_images(self, obj):
        qs = obj.images.all().order_by('order')
        return InternationalRatingImageSerializer(qs, many=True, context=self.context).data


class NationalRatingSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = NationalRating
        fields = ['id', 'slug', 'name', 'title', 'description', 'images', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {
            'uz': obj.name_uz or '',
            'ru': obj.name_ru or obj.name_uz or '',
            'en': obj.name_en or obj.name_uz or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {
            'uz': obj.title_uz or '',
            'ru': obj.title_ru or obj.title_uz or '',
            'en': obj.title_en or obj.title_uz or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {
            'uz': obj.description_uz or '',
            'ru': obj.description_ru or obj.description_uz or '',
            'en': obj.description_en or obj.description_uz or '',
        }

    @extend_schema_field(NationalRatingImageSerializer(many=True))
    def get_images(self, obj):
        qs = obj.images.all().order_by('order')
        return NationalRatingImageSerializer(qs, many=True, context=self.context).data


class InternationalPostSerializer(serializers.ModelSerializer):
    title      = serializers.SerializerMethodField()
    content    = serializers.SerializerMethodField()
    image      = serializers.SerializerMethodField()
    images     = serializers.SerializerMethodField()
    type_label = serializers.CharField(source='get_post_type_display', read_only=True)

    class Meta:
        model  = InternationalPost
        fields = ['id', 'slug', 'post_type', 'type_label', 'title', 'content', 'image', 'images', 'date', 'order', 'created_at', 'updated_at']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        req = self.context.get('request')
        lang = self._lang()
        localized = getattr(obj, f'image_{lang}', None) if lang != 'uz' else None
        return _abs_url(req, localized) or _abs_url(req, obj.image)

    @extend_schema_field(InternationalPostImageSerializer(many=True))
    def get_images(self, obj):
        qs = obj.images.all().order_by('order')
        return InternationalPostImageSerializer(qs, many=True, context=self.context).data


class AkademikAlmashinuvRasmSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    caption   = serializers.SerializerMethodField()

    class Meta:
        model  = AkademikAlmashinuvRasm
        fields = ['id', 'image_url', 'caption', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_image_url(self, obj):
        req = self.context.get('request')
        uz = _abs_url(req, obj.image)
        ru = _abs_url(req, obj.image_ru) if obj.image_ru else uz
        en = _abs_url(req, obj.image_en) if obj.image_en else uz
        return {'uz': uz, 'ru': ru, 'en': en}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_caption(self, obj):
        return {'uz': obj.caption_uz, 'ru': obj.caption_ru or obj.caption_uz, 'en': obj.caption_en or obj.caption_uz}


class AkademikAlmashinuvSerializer(serializers.ModelSerializer):
    title  = serializers.SerializerMethodField()
    body   = serializers.SerializerMethodField()
    rasmlar = serializers.SerializerMethodField()

    class Meta:
        model  = AkademikAlmashinuv
        fields = ['id', 'slug', 'title', 'body', 'rasmlar', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_body(self, obj):
        return {'uz': obj.body_uz, 'ru': obj.body_ru or obj.body_uz, 'en': obj.body_en or obj.body_uz}

    @extend_schema_field(AkademikAlmashinuvRasmSerializer(many=True))
    def get_rasmlar(self, obj):
        return AkademikAlmashinuvRasmSerializer(
            obj.rasmlar.all(), many=True, context=self.context
        ).data


class XalqaroReytingBolimRasmSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = XalqaroReytingBolimRasm
        fields = ['id', 'image_url', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class XalqaroReytingBolimSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    rasmlar     = serializers.SerializerMethodField()

    class Meta:
        model  = XalqaroReytingBolim
        fields = ['id', 'slug', 'bolim_type', 'title', 'description', 'image_url', 'rasmlar', 'link', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(XalqaroReytingBolimRasmSerializer(many=True))
    def get_rasmlar(self, obj):
        qs = obj.rasmlar.all().order_by('order')
        return XalqaroReytingBolimRasmSerializer(qs, many=True, context=self.context).data


# ─────────────────────── Xorijlik Professor-o'qituvchilar ───────────────────────

class XorijlikProfessorSerializer(serializers.ModelSerializer):
    bio             = serializers.SerializerMethodField()
    education       = serializers.SerializerMethodField()
    specialty       = serializers.SerializerMethodField()
    academic_degree = serializers.SerializerMethodField()
    academic_title  = serializers.SerializerMethodField()
    photo_url       = serializers.SerializerMethodField()

    class Meta:
        model  = XorijlikProfessor
        fields = [
            'id', 'slug', 'full_name', 'photo_url', 'country', 'from_year',
            'bio', 'education', 'specialty',
            'academic_degree', 'academic_title',
            'order', 'created_at', 'updated_at',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_bio(self, obj):
        return getattr(obj, f'bio_{self._lang()}') or obj.bio_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_education(self, obj):
        return getattr(obj, f'education_{self._lang()}') or obj.education_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_specialty(self, obj):
        return getattr(obj, f'specialty_{self._lang()}') or obj.specialty_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_academic_degree(self, obj):
        return getattr(obj, f'academic_degree_{self._lang()}') or obj.academic_degree_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_academic_title(self, obj):
        return getattr(obj, f'academic_title_{self._lang()}') or obj.academic_title_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_photo_url(self, obj):
        return _abs_url(self.context.get('request'), obj.photo)


class StudyInUzbekistanConfigSerializer(serializers.ModelSerializer):
    intro          = serializers.SerializerMethodField()
    banner_image   = serializers.SerializerMethodField()
    banner_caption = serializers.SerializerMethodField()
    announcement   = serializers.SerializerMethodField()
    portal_button  = serializers.SerializerMethodField()

    class Meta:
        model  = StudyInUzbekistanConfig
        fields = [
            'intro',
            'banner_image', 'banner_link', 'banner_caption',
            'announcement',
            'portal_url', 'portal_button',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_intro(self, obj):
        return getattr(obj, f'intro_{self._lang()}') or obj.intro_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_banner_image(self, obj):
        if not obj.banner_image:
            return None
        return _abs_url(self.context.get('request'), obj.banner_image)

    @extend_schema_field(OpenApiTypes.STR)
    def get_banner_caption(self, obj):
        return getattr(obj, f'banner_caption_{self._lang()}') or obj.banner_caption_uz

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_announcement(self, obj):
        if not obj.announcement_show:
            return None
        lang = self._lang()
        return {
            'show':      obj.announcement_show,
            'variant':   obj.announcement_variant,
            'icon':      obj.announcement_icon,
            'title':     getattr(obj, f'announcement_title_{lang}') or obj.announcement_title_uz,
            'text':      getattr(obj, f'announcement_text_{lang}') or obj.announcement_text_uz,
            'link':      obj.announcement_link,
            'link_text': obj.announcement_link_text,
        }

    @extend_schema_field(OpenApiTypes.STR)
    def get_portal_button(self, obj):
        lang = self._lang()
        return getattr(obj, f'portal_button_{lang}') or obj.portal_button_uz or 'Study in Uzbekistan'
