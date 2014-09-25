from rest_framework import serializers

from dataentry.models import GeoCodeLocation


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District


class VDCSerializer(serializer.ModelSerializer):
	class Meta:
		model = VDC