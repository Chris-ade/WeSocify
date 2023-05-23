from rest_framework import serializers
from .models import *

class MomentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomentImages
        fields = "__all__"

class MomentSerializer(serializers.ModelSerializer):
    images = MomentImageSerializer(many=True)

    def get_moment_images(self, instance):
    	qs = MomentImages.objects.filter(moment__id=instance.id)
    	data = MomentImageSerializer(qs, many=True).data
    	return data

    class Meta:
        model = Moment
        fields = "__all__"