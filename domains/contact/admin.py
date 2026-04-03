from django.contrib import admin

from .models import FAQ, RectorAppeal


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ('short_question', 'vote_count', 'is_answered', 'is_published', 'created_at')
    list_editable = ('is_answered', 'is_published')
    list_filter   = ('is_answered', 'is_published')
    search_fields = ('question_uz', 'question_ru', 'question_en')
    readonly_fields = ('vote_count', 'created_at', 'updated_at')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 SAVOL-JAVOB (FAQ)</strong> — '
                'Foydalanuvchilar saytda savol yuboradi, admin panelda javob yoziladi.<br>'
                '<span style="color:#c62828;">'
                '• <strong>Savol</strong> — foydalanuvchi yoki admin tomonidan<br>'
                '• <strong>Javob</strong> — admin panelda shu yerda yoziladi<br>'
                '• <strong>Ko\'p berilgan savollar</strong> birinchi chiqadi (vote_count bo\'yicha)<br>'
                '• <strong>Javoblangan</strong> — belgini qo\'ying, aks holda frontend da ko\'rinmaydi'
                '</span>'
                '</div>'
            ),
        }),
        ("Savol", {'fields': ('question_uz', 'question_ru', 'question_en')}),
        ("Javob", {'fields': ('answer_uz', 'answer_ru', 'answer_en')}),
        ("Holat", {'fields': ('is_answered', 'is_published', 'vote_count')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description="Savol")
    def short_question(self, obj):
        return obj.question_uz[:80] + ('...' if len(obj.question_uz) > 80 else '')


@admin.register(RectorAppeal)
class RectorAppealAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'email', 'phone', 'faculty', 'status', 'created_at')
    list_filter   = ('status',)
    list_editable = ('status',)
    search_fields = ('full_name', 'email', 'phone', 'faculty')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 REKTORGA MUROJAAT</strong> — '
                'Foydalanuvchilar saytdagi forma orqali yuboradi (POST). Bu yerda faqat <strong>o\'qish va javob berish</strong>.<br>'
                '<span style="color:#c62828;">'
                'Holat: <strong>Yangi</strong> → Ko\'rib chiqilmoqda → <strong>Javob berildi</strong> deb o\'zgartiring.'
                '</span>'
                '</div>'
            ),
        }),
        ("Murojaat egasi", {'fields': ('full_name', 'email', 'phone', 'faculty', 'group', 'birth_date')}),
        ("Murojaat", {'fields': ('message',)}),
        ("Holat", {'fields': ('status',)}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )
