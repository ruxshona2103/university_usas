from rest_framework import serializers

from domains.academic.models import Staff


class StaffSerializer(serializers.ModelSerializer):
	title = serializers.SerializerMethodField()
	position = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	page_slug = serializers.SerializerMethodField()
	page_url = serializers.SerializerMethodField()

	class Meta:
		model = Staff
		fields = [
			'id',
			'is_head',
			'role',
			'title',
			'full_name',
			'position',
			'description',
			'image',
			'address',
			'reception',
			'phone',
			'fax',
			'email',
			'order',
			'page_slug',
			'page_url',
		]

	def _lang(self):
		return self.context.get('lang', 'uz')

	def get_title(self, obj):
		lang = self._lang()
		return getattr(obj, f'title_{lang}', obj.title_uz) or obj.title_uz

	def get_position(self, obj):
		lang = self._lang()
		return getattr(obj, f'position_{lang}', obj.position_uz) or obj.position_uz

	def get_description(self, obj):
		return {
			'uz': obj.description_uz,
			'ru': obj.description_ru,
			'en': obj.description_en,
		}

	def get_image(self, obj):
		if not obj.image:
			return None
		try:
			image_url = obj.image.url
		except Exception:
			return None
		request = self.context.get('request')
		if request:
			return request.build_absolute_uri(image_url)
		return image_url

	def get_page_slug(self, obj):
		if obj.navbar_item_id:
			return obj.navbar_item.slug
		return None

	def get_page_url(self, obj):
		if obj.navbar_item_id:
			return f'/page/{obj.navbar_item.slug}'
		return None
