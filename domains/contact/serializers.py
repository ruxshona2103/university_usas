from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.contact.models import FAQ, RectorAppeal, RectorAppealExtraField, ContactMessage


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer   = serializers.SerializerMethodField()
    likes    = serializers.IntegerField(source='vote_count', read_only=True)

    class Meta:
        model  = FAQ
        fields = [
            'id',
            'question', 'answer',
            'views', 'likes', 'comments',
            'vote_count',
            'is_answered',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_question(self, obj):
        lang = self._lang()
        return getattr(obj, f'question_{lang}') or obj.question_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_answer(self, obj):
        lang = self._lang()
        return getattr(obj, f'answer_{lang}') or obj.answer_uz


class FAQCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FAQ
        fields = ['question_uz', 'question_ru', 'question_en']


class RectorAppealExtraFieldSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model  = RectorAppealExtraField
        fields = ['field_key', 'label', 'field_type', 'is_required', 'order']

    def get_label(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'label_{lang}') or obj.label_uz


class RectorAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RectorAppeal
        fields = [
            'sender_type', 'appeal_type',
            'full_name', 'email', 'phone',
            'faculty', 'group', 'birth_date',
            'message', 'extra_data',
        ]

    def validate(self, attrs):
        sender_type = attrs.get('sender_type', RectorAppeal.SenderType.STUDENT)
        if sender_type == RectorAppeal.SenderType.STUDENT:
            if not attrs.get('faculty', '').strip():
                raise serializers.ValidationError({'faculty': 'Talaba uchun fakultet majburiy.'})
            if not attrs.get('group', '').strip():
                raise serializers.ValidationError({'group': 'Talaba uchun guruh majburiy.'})
        else:
            attrs.setdefault('faculty', '')
            attrs.setdefault('group', '')

        extra_data = attrs.get('extra_data', {})
        required_keys = list(
            RectorAppealExtraField.objects.filter(is_active=True, is_required=True).values_list('field_key', flat=True)
        )
        missing = [k for k in required_keys if not extra_data.get(k, '')]
        if missing:
            raise serializers.ValidationError({'extra_data': f'Majburiy maydonlar to\'ldirilmagan: {", ".join(missing)}'})
        return attrs


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['full_name', 'email', 'phone', 'subject', 'message']


from domains.contact.models import QabulRaqami


class QabulRaqamiSerializer(serializers.ModelSerializer):
    class Meta:
        model  = QabulRaqami
        fields = ['id', 'number', 'created_at', 'updated_at']
