from apps.sensors.models import *
from rest_framework import serializers
from apps.company.serializers import *
class config_tipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_tipo_sensor
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = sensor
        fields = '__all__'
    fk_IdTipo = config_tipoSerializer()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = register
        fields = '__all__'
    fk_IdSensor = SensorSerializer()

class dispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = dispositivo
        fields = '__all__'
    
    IdArea = Area_trabajoSerializer()

class registro_incidenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = registro_incidencias
        fields = '__all__'