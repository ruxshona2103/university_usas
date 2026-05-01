from django.contrib import admin

from .models import FAQ, RectorAppeal


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ('short_question', 'vote_count', 'views', 'comments', 'is_answered', 'is_published', 'created_at')
    list_editable = ('is_answered', 'is_published')
    list_filter   = ('is_answered', 'is_published')
    search_fields = ('question_uz', 'question_ru', 'question_en')
    readonly_fields = ('vote_count', 'views', 'comments', 'created_at', 'updated_at')

    fieldsets = (
        ("Savol", {'fields': ('question_uz', 'question_ru', 'question_en')}),
        ("Javob", {'fields': ('answer_uz', 'answer_ru', 'answer_en')}),
        ("Holat", {'fields': ('is_answered', 'is_published', 'vote_count')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('views', 'comments', 'created_at', 'updated_at')}),
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
        ("Murojaat egasi", {'fields': ('full_name', 'email', 'phone', 'faculty', 'group', 'birth_date')}),
        ("Murojaat", {'fields': ('message',)}),
        ("Holat", {'fields': ('status',)}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

from .models import QabulRaqami

@admin.register(QabulRaqami)
class QabulRaqamiAdmin(admin.ModelAdmin):
    list_display  = ('number', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('number',)
