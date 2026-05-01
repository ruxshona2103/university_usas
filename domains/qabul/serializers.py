from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from .models import (
    QabulBolim, QabulBolimItem,
    QabulKomissiyaTarkibi,
    QabulKuni,
    CallCenter,
    QabulYangilik,
    QabulNarx,
    QabulHujjat,
    QabulNavbar, QabulNavbarItem,
)


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


def _lang(context):
    return context.get('lang', 'uz')


# ─────────────────────────── Qabul Bo'lim ───────────────────────────

class QabulBolimItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    body  = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model  = QabulBolimItem
        fields = ['id', 'item_type', 'title', 'body', 'file_url', 'link', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_body(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'body_{lang}') or obj.body_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_file_url(self, obj):
        return _abs_url(self.context.get('request'), obj.file)


class QabulBolimSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    items       = serializers.SerializerMethodField()

    class Meta:
        model  = QabulBolim
        fields = ['id', 'slug', 'bolim_type', 'title', 'description', 'items', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'description_{lang}') or obj.description_uz

    @extend_schema_field(QabulBolimItemSerializer(many=True))
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return QabulBolimItemSerializer(qs, many=True, context=self.context).data


# ─────────────────────────── Komissiya ───────────────────────────

class QabulKomissiyaTarkibiSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model  = QabulKomissiyaTarkibi
        fields = ['id', 'full_name', 'position', 'phone', 'email', 'photo_url', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'full_name_{lang}') or obj.full_name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'position_{lang}') or obj.position_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_photo_url(self, obj):
        return _abs_url(self.context.get('request'), obj.photo)


# ─────────────────────────── Qabul Kunlari ───────────────────────────

class QabulKuniSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    qabul_type_label = serializers.CharField(source='get_qabul_type_display', read_only=True)

    class Meta:
        model  = QabulKuni
        fields = [
            'id', 'qabul_type', 'qabul_type_label', 'title',
            'start_date', 'end_date', 'description',
            'order', 'created_at', 'updated_at',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'description_{lang}') or obj.description_uz


# ─────────────────────────── Call Center ───────────────────────────

class CallCenterSerializer(serializers.ModelSerializer):
    label         = serializers.SerializerMethodField()
    working_hours = serializers.SerializerMethodField()

    class Meta:
        model  = CallCenter
        fields = ['id', 'phone', 'label', 'working_hours', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.STR)
    def get_label(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'label_{lang}') or obj.label_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_working_hours(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'working_hours_{lang}') or obj.working_hours_uz


# ─────────────────────────── Yangiliklar ───────────────────────────

class QabulYangilikSerializer(serializers.ModelSerializer):
    title    = serializers.SerializerMethodField()
    body     = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = QabulYangilik
        fields = ['id', 'title', 'body', 'image_url', 'date', 'views', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_body(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'body_{lang}') or obj.body_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


# ─────────────────────────── Kontrakt Narxlari ───────────────────────────

class QabulNarxSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    edu_type_label = serializers.CharField(source='get_edu_type_display', read_only=True)
    edu_form_label = serializers.CharField(source='get_edu_form_display', read_only=True)

    class Meta:
        model  = QabulNarx
        fields = [
            'id', 'edu_type', 'edu_type_label', 'edu_form', 'edu_form_label',
            'specialty_code', 'specialty_name', 'price', 'year',
            'order', 'created_at', 'updated_at',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_specialty_name(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'specialty_name_{lang}') or obj.specialty_name_uz


# ─────────────────────────── Hujjatlar ───────────────────────────

class QabulHujjatSerializer(serializers.ModelSerializer):
    title        = serializers.SerializerMethodField()
    description  = serializers.SerializerMethodField()
    file_url     = serializers.SerializerMethodField()
    hujjat_type_label = serializers.CharField(source='get_hujjat_type_display', read_only=True)

    class Meta:
        model  = QabulHujjat
        fields = [
            'id', 'hujjat_type', 'hujjat_type_label',
            'title', 'description', 'file_url',
            'order', 'created_at', 'updated_at',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'description_{lang}') or obj.description_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_file_url(self, obj):
        return _abs_url(self.context.get('request'), obj.file)


# ─────────────────────────── Qabul Navbar ───────────────────────────

class QabulNavbarItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = QabulNavbarItem
        fields = ['id', 'slug', 'title', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz


class QabulNavbarSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = QabulNavbar
        fields = ['id', 'slug', 'title', 'items', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = _lang(self.context)
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(QabulNavbarItemSerializer(many=True))
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return QabulNavbarItemSerializer(qs, many=True, context=self.context).data
