from apps.company.models import *
from apps.memberships.serializers import *
from rest_framework import serializers

class configSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_web_empresa
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'

    fk_config = configSerializer()

class Rl_user_companySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rl_user_company
        fields = '__all__'
    fk_IdEmpresa  = CompanySerializer()

class regionSerializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = '__all__'

class Rl_sucursal_licenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = '__all__'
    fk_IdLicencia = licenciaSerializer()

class Area_trabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area_trabajo
        fields = '__all__'

