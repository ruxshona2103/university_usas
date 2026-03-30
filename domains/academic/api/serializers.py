from rest_framework import serializers

from domains.academic.models import OrganizationUnit, Staff


class StaffSerializer(serializers.ModelSerializer):
	title = serializers.SerializerMethodField()
	position = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()

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


class OrganizationUnitTreeSerializer(serializers.ModelSerializer):
	title = serializers.SerializerMethodField()
	children = serializers.SerializerMethodField()

	class Meta:
		model = OrganizationUnit
		fields = [
			'id',
			'title',
			'unit_type',
			'slug',
			'has_own_page',
			'is_featured',
			'order',
			'children',
		]

	def get_title(self, obj):
		lang = self.context.get('lang', 'uz')
		return getattr(obj, f'title_{lang}', obj.title_uz) or obj.title_uz

	def get_children(self, obj):
		children = obj.children.filter(is_active=True).order_by('order', 'created_at')
		serializer = OrganizationUnitTreeSerializer(children, many=True, context=self.context)
		return serializer.data


class OrganizationUnitDetailSerializer(serializers.ModelSerializer):
	title = serializers.SerializerMethodField()
	content = serializers.SerializerMethodField()
	staff = serializers.SerializerMethodField()
	children = serializers.SerializerMethodField()
	breadcrumb = serializers.SerializerMethodField()

	class Meta:
		model = OrganizationUnit
		fields = [
			'id',
			'title',
			'title_ru',
			'title_en',
			'unit_type',
			'slug',
			'content',
			'has_own_page',
			'is_featured',
			'order',
			'staff',
			'children',
			'breadcrumb',
		]

	def _lang(self):
		return self.context.get('lang', 'uz')

	def get_title(self, obj):
		lang = self._lang()
		return getattr(obj, f'title_{lang}', obj.title_uz) or obj.title_uz

	def get_content(self, obj):
		lang = self._lang()
		return getattr(obj, f'content_{lang}', obj.content_uz) or obj.content_uz

	def get_staff(self, obj):
		queryset = obj.staff.filter(is_active=True).order_by('-is_head', 'order', 'created_at')
		return StaffSerializer(queryset, many=True, context=self.context).data

	def get_children(self, obj):
		queryset = obj.children.filter(is_active=True).order_by('order', 'created_at')
		return OrganizationUnitTreeSerializer(queryset, many=True, context=self.context).data

	def get_breadcrumb(self, obj):
		lang = self._lang()
		chain = []
		current = obj
		while current is not None:
			chain.append(current)
			current = current.parent
		chain.reverse()
		return [
			{
				'title': getattr(item, f'title_{lang}', item.title_uz) or item.title_uz,
				'slug': item.slug,
			}
			for item in chain
		]
