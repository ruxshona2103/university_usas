from rest_framework import serializers

from domains.activities.models import ContractPrice, ServiceVehicle


class ContractPriceSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    education_type = serializers.CharField(source='get_education_type_display')
    education_form = serializers.CharField(source='get_education_form_display')

    class Meta:
        model  = ContractPrice
        fields = [
            'id', 'specialty_code', 'specialty_name',
            'education_type', 'education_form',
            'price', 'order',
        ]

    def get_specialty_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'specialty_name_{lang}') or obj.specialty_name_uz


class ServiceVehicleSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.SerializerMethodField()
    fuel_type    = serializers.CharField(source='get_fuel_type_display')

    class Meta:
        model  = ServiceVehicle
        fields = [
            'id', 'name', 'vehicle_type',
            'manufactured_year', 'fuel_type', 'order',
        ]

    def get_vehicle_type(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'vehicle_type_{lang}') or obj.vehicle_type_uz
