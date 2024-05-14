from apps.sensors.models import *
from rest_framework import serializers

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = register
        fields = '__all__'

class config_tipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_tipo_sensor
        fields = '__all__'

class dispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = dispositivo
        fields = '__all__'

class registro_incidenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = registro_incidencias
        fields = '__all__'