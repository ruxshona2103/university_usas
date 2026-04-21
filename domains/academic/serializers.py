from rest_framework import serializers

from domains.academic.models import AcademyStat


class AcademyStatSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model  = AcademyStat
        fields = ['id', 'label', 'value', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_label(self, obj):
        lang = self._lang()
        return getattr(obj, f'label_{lang}') or obj.label_uz

    def get_value(self, obj):
        lang = self._lang()
        return getattr(obj, f'value_{lang}') or obj.value_uz
