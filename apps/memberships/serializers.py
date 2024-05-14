from apps.memberships.models import *
from rest_framework import serializers

class licenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licencia
        fields = '__all__'