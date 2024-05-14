import os
from django.conf import settings
import uuid
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from apps.accounts.models import *
from .models import *
from .serializers import *
import traceback  # Para obtener la traza completa del error
from rest_framework.parsers import MultiPartParser, FormParser #Para la carga de archivos

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = company.objects.all()
    serializer_class = CompanySerializer
    
    @action(detail=False, methods=['post'], url_path='create-company', url_name='sensor')
    def create_company(self, request):
        try:
            nombre_empresa = request.data.get('Nombre_Empresa')
            imagen_empresa = request.data.get('Url_img')
            
            # Comprobar si la empresa ya existe
            if company.objects.filter(Nombre_Empresa=nombre_empresa).exists():
                return Response({"Error": "La empresa no se pudo crear porque ya existe una con ese nombre."})
            
            # Verificar si se proporcionó una imagen
            if imagen_empresa:
                # Guardar la imagen en la carpeta de medios
                nombre_imagen = f"empresa_{nombre_empresa}_{uuid.uuid4()}.{imagen_empresa.name.split('.')[-1]}"
                ruta_imagen = os.path.join(settings.MEDIA_ROOT, nombre_imagen)
                with open(ruta_imagen, 'wb+') as destino:
                    for chunk in imagen_empresa.chunks():
                        destino.write(chunk)
            else:
                nombre_imagen = None
            
            # Obtener el usuario y la configuración asociada
            email_usuario = request.data.get('email')
            usuario = User.objects.get(email=email_usuario)
            configuracion = config_web_empresa.objects.get(IdConfig=1)

            # Crear la empresa con los datos proporcionados
            nueva_empresa = company.objects.create(
                Nombre_Empresa=nombre_empresa,
                Url_img=nombre_imagen,  # Guardar la ruta de la imagen
                fk_config=configuracion
            )

            # Crear la relación entre el usuario y la empresa
            Rl_user_company.objects.create(
                fk_IdUsuario=usuario,
                fk_IdEmpresa=nueva_empresa
            )

            return Response({
                "message": "Empresa creada exitosamente"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Manejar cualquier excepción y devolver información sobre el error
            error_message = str(e)  # Obtener el mensaje de error
            error_trace = traceback.format_exc()  # Obtener la traza completa del error

            return Response(
                {
                    "error": "Error al crear el registro",
                    "message": error_message,
                    "trace": error_trace
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )