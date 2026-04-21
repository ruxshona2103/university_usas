from rest_framework import serializers
from domains.contact.models import FAQ, RectorAppeal


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

    def get_question(self, obj):
        lang = self._lang()
        return getattr(obj, f'question_{lang}') or obj.question_uz

    def get_answer(self, obj):
        lang = self._lang()
        return getattr(obj, f'answer_{lang}') or obj.answer_uz


class FAQCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FAQ
        fields = ['question_uz', 'question_ru', 'question_en']


class RectorAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RectorAppeal
        fields = ['full_name', 'email', 'phone', 'faculty', 'group', 'birth_date', 'message']
