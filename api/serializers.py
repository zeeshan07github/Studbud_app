from rest_framework.serializers import ModelSerializer
from studbud.models import room

class roomserializer(ModelSerializer):
    class Meta:
        model= room
        fields = '__all__'