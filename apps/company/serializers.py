from apps.company.models import *
from apps.memberships.serializers import *
from apps.accounts.serializers import *
from rest_framework import serializers

class configSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_web_empresa
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'
        extra_kwargs = {
            'IdEmpresa': {'read_only': True},  # Permitir que el campo IdEmpresa sea escribible
        }

class Rl_user_companySerializer(serializers.ModelSerializer):
    fk_IdEmpresa = CompanySerializer()  # Definir el campo utilizando CompanySerializer

    class Meta:
        model = Rl_user_company
        fields = '__all__'
        
class Rl_company_userSerializer(serializers.ModelSerializer):
    fk_IdUsuario = UserSerializer()  # Definir el campo utilizando CompanySerializer

    class Meta:
        model = Rl_user_company
        fields = '__all__'

class regionSerializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = '__all__'

class sucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'
        
class Rl_sucursal_licenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = '__all__'
    # fk_IdLicencia = licenciaSerializer()

class Area_trabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area_trabajo
        fields = '__all__'

