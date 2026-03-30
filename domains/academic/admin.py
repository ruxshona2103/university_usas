from django.contrib import admin

from .models import OrganizationUnit, Staff


class StaffInline(admin.TabularInline):
	model = Staff
	extra = 0
	fields = (
		'full_name',
		'role',
		'is_head',
		'title_uz',
		'phone',
		'email',
		'order',
		'is_active',
	)
	ordering = ('order',)
	show_change_link = True


@admin.register(OrganizationUnit)
class OrganizationUnitAdmin(admin.ModelAdmin):
	list_display = (
		'title_uz',
		'unit_type',
		'parent',
		'has_own_page',
		'is_featured',
		'order',
		'is_active',
	)
	list_filter = ('unit_type', 'is_active', 'has_own_page', 'is_featured')
	search_fields = ('title_uz', 'title_ru', 'title_en', 'slug')
	list_editable = ('order', 'is_active', 'has_own_page', 'is_featured')
	readonly_fields = ('slug', 'created_at', 'updated_at')
	ordering = ('order', 'created_at')
	inlines = [StaffInline]

	fieldsets = (
		("Nomlar", {
			'fields': ('title_uz', 'title_ru', 'title_en')
		}),
		("Tuzilma", {
			'fields': ('unit_type', 'parent', 'order')
		}),
		("Sahifa sozlamalari", {
			'fields': ('has_own_page', 'is_featured', 'is_active')
		}),
		("Kontent", {
			'fields': ('content_uz', 'content_ru', 'content_en')
		}),
		("Texnik", {
			'classes': ('collapse',),
			'fields': ('slug', 'created_at', 'updated_at')
		}),
	)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
	list_display = (
		'full_name',
		'unit',
		'role',
		'is_head',
		'phone',
		'email',
		'order',
		'is_active',
	)
	list_filter = ('role', 'is_active', 'is_head', 'unit__unit_type')
	search_fields = ('full_name', 'title_uz', 'title_ru', 'title_en', 'email', 'phone')
	list_editable = ('order', 'is_active', 'is_head')
	ordering = ('order', 'created_at')
	readonly_fields = ('created_at', 'updated_at')

	fieldsets = (
		("Bo'lim va rol", {
			'fields': ('unit', 'role', 'is_head', 'order', 'is_active')
		}),
		("Lavozim va ism", {
			'fields': ('title_uz', 'title_ru', 'title_en', 'full_name')
		}),
		("Ilmiy unvon", {
			'fields': ('position_uz', 'position_ru', 'position_en')
		}),
		("Aloqa", {
			'fields': ('address', 'reception', 'phone', 'fax', 'email')
		}),
		("Batafsil", {
			'fields': ('description_uz', 'description_ru', 'description_en')
		}),
		("Rasm", {
			'fields': ('image',)
		}),
		("Texnik", {
			'classes': ('collapse',),
			'fields': ('created_at', 'updated_at')
		}),
	)
