import os
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from apps.accounts.models import *
from apps.sensors.models import *
from apps.sensors.serializers import *
from .models import *
from .serializers import *
import traceback  # Para obtener la traza completa del error
from rest_framework.parsers import MultiPartParser, FormParser #Para la carga de archivos
import hashlib #libreria de encryptado
from datetime import timedelta
from django.utils import timezone

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii
# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = company.objects.all()
    serializer_class = CompanySerializer
    
    @action(detail=False, methods=['post'], url_path='create-company', url_name='sensor')
    def create_company(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Validar si ya existe una empresa con el mismo nombre
            nombre_empresa = serializer.validated_data.get('Nombre_Empresa')
            if company.objects.filter(Nombre_Empresa=nombre_empresa).exists():
                # Si ya existe una empresa con el mismo nombre, devolver un error
                return Response({'error': 'Ya existe una empresa con el mismo nombre.'}, status=status.HTTP_400_BAD_REQUEST)
            # Encriptar el nombre de la empresa utilizando SHA-256
            nombre_empresa_encriptado = hashlib.sha256(nombre_empresa.encode()).hexdigest()
            #convertir y guardar modelo
             # Asignar el nombre de la empresa encriptado al campo ClaveEmpresa
            validated_data['ClaveEmpresa'] = nombre_empresa_encriptado
            
            empresa = company(**validated_data)
            empresa.save()
            queryuser = User.objects.get(email = request.data.get('email'))
            relacion = Rl_user_company.objects.create(
                 fk_IdUsuario=queryuser,
                 fk_IdEmpresa=empresa
             )
            serializer_response = CompanySerializer(empresa)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['get'], url_path='user-companies', url_name='user_companies')
    def user_companies(self, request):
        try:
            # Obtener el usuario a partir de la solicitud
            email_usuario = request.query_params.get('email')
            usuario = User.objects.get(email=email_usuario)
            
            # Obtener las empresas asociadas al usuario
            empresas_usuario = Rl_user_company.objects.filter(fk_IdUsuario=usuario)
            empresas = []
            for relacion in empresas_usuario:
                print(f"{settings.MEDIA_ROOT}{relacion.fk_IdEmpresa.Url_img}")
                empresa_info = {
                    "IdEmpresa": relacion.fk_IdEmpresa.IdEmpresa,
                    "Nombre_Empresa": relacion.fk_IdEmpresa.Nombre_Empresa,
                    "ClaveEmpresa": relacion.fk_IdEmpresa.ClaveEmpresa,
                    "Url_img": f"{settings.MEDIA_URL}{relacion.fk_IdEmpresa.Url_img}" if relacion.fk_IdEmpresa.Url_img else None,
                    # Agrega cualquier otro campo que quieras devolver
                }
                empresas.append(empresa_info)

            return Response(empresas, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"Error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            error_message = str(e)
            error_trace = traceback.format_exc()

            return Response(
                {
                    "error": "Error al obtener las empresas del usuario.",
                    "message": error_message,
                    "trace": error_trace
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=False, methods=['post'], url_path='delete-company-by-name', url_name='delete-company-by-name')
    def delete_company_by_name(self, request):
        # Obtener la URL de la imagen a partir de los datos de la solicitud
        idempresa = request.query_params.get('IdEmpresa')
        
        # Buscar la empresa basada en la URL de la imagen
        try:
            empresa = company.objects.get(IdEmpresa=idempresa)
        except company.DoesNotExist:
            return Response({'detail': 'Empresa no encontrada por el id proporcionado'}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar la imagen asociada si existe
        if empresa.Url_img:
            empresa.Url_img.delete()  # Eliminar la imagen del sistema de archivos

        # Eliminar el registro de la empresa
        empresa.delete()
        
        return Response({'detail': 'Empresa e imagen asociada eliminadas correctamente.'}, status=status.HTTP_204_NO_CONTENT)
    
class RegionViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = region.objects.all()
    serializer_class = regionSerializer
    
    @action(detail=False, methods=['post'], url_path='create-region', url_name='create-region')
    def create_region(self, request):
        serializer = regionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Validar si ya existe una empresa con el mismo nombre
            print(validated_data)
            nombre_region = serializer.validated_data.get('Nombre_region')
            idempresa = serializer.validated_data.get('fk_IdEmpresa')
            if region.objects.filter(Nombre_region=nombre_region, fk_IdEmpresa=idempresa).exists():
                # Si ya existe una empresa con el mismo nombre, devolver un error
                return Response({'error': 'Ya existe una region registrada con estos datos'}, status=status.HTTP_400_BAD_REQUEST)
            #convertir y guardar modelo
            reg = region(**validated_data)
            reg.save()
            serializer_response = regionSerializer(reg)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='get-regions-by-company', url_name='get-regions-by-company')
    def get_regions_by_company(self, request):
        # Obtener el ID de la empresa de los parámetros de la solicitud
        idempresa = request.query_params.get('IdEmpresa')
        
        # Validar si se proporcionó el ID de la empresa en los parámetros de la solicitud
        if not idempresa:
            return Response({'error': 'Se requiere proporcionar el ID de la empresa.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtener todas las regiones asociadas a la empresa especificada
            regions = region.objects.filter(fk_IdEmpresa=idempresa)
            # Serializar las regiones encontradas
            serializer = regionSerializer(regions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], url_path='delete-region', url_name='delete-region')
    def delete_region(self, request):
        # Obtener la URL de la imagen a partir de los datos de la solicitud
        idregion = request.query_params.get('IdRegion')
        
        # Buscar la empresa basada en la URL de la imagen
        try:
            Region = region.objects.get(IdRegion=idregion)
        except company.DoesNotExist:
            return Response({'detail': 'Empresa no encontrada por el id proporcionado'}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar la imagen asociada si existe
        if Region.ImagenEmpresa:
            Region.ImagenEmpresa.delete()  # Eliminar la imagen del sistema de archivos

        # Eliminar el registro de la empresa
        Region.delete()
        
        return Response({'detail': 'Empresa e imagen asociada eliminadas correctamente.'}, status=status.HTTP_204_NO_CONTENT)

class SucursalViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Sucursal.objects.all()
    serializer_class = sucursalSerializer

    @action(detail=False, methods=['post'], url_path='create-sucursal', url_name='create-sucursal')
    def create_sucursal(self, request):
        def decrypt_from_hex(encrypted_text_hex, key):
            encrypted_data = binascii.unhexlify(encrypted_text_hex.encode())
            iv = encrypted_data[:16]  # Extraer el IV
            ct_bytes = encrypted_data[16:]

            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            decrypted_data = unpad(cipher.decrypt(ct_bytes), AES.block_size)
            return decrypted_data.decode('utf-8')
        
        serializer = sucursalSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Validar si ya existe una sucursal con el mismo nombre
            print(validated_data)
            nombre_region = serializer.validated_data.get('Nombre_sucursal')
            idregion = serializer.validated_data.get('fk_IdRegion')
            if Sucursal.objects.filter(Nombre_sucursal=nombre_region, fk_IdRegion=idregion).exists():
                # Si ya existe una empresa con el mismo nombre, devolver un error
                return Response({'error': 'Ya existe una sucursal registrada con estos datos'}, status=status.HTTP_302_FOUND)
            #convertir y guardar modelo
            reg = Sucursal(**validated_data)
            reg.save()
            serializer_response = sucursalSerializer(reg)
            
            #obtener la licencia
            licencia = request.data.get('Licencia')
            encryption_key_hex = '300d960a707396f529f0e6ab0cb27f4469e09fa215be10e0cdb80a40cbe2c6ed'
            encryption_key = binascii.unhexlify(encryption_key_hex)
            
            #validar si la licencia proporcionada existe
            try:
                
                print(licencia)
                querylicencia=Licencia.objects.get(Licencia=licencia)
                #se desencripta la licencia
                print("si lo encontró")
                decrypted_text = decrypt_from_hex(licencia, encryption_key)
                print(f"Texto desencriptado: {decrypted_text}")
                
                partes_licencia = decrypted_text.split('/')
                dias_vencimiento = int(partes_licencia[0])
                
                # Calcular la fecha de vencimiento
                fecha_vencimiento = timezone.now() + timedelta(days=dias_vencimiento)
                
                create = Rl_sucursal_licencia.objects.create(
                    fk_IdSucursal = reg,
                    fk_IdLicencia = querylicencia,
                    Fecha_vencimiento = fecha_vencimiento
                )
                
                print(querylicencia.Estado_licencia)
                querylicencia.Estado_licencia='vigente'
                querylicencia.save()
                
            except:
                fecha_vencimiento = timezone.now() + timedelta(days=7)
                licenciaasignada= Licencia.objects.get(Licencia='LicenciaDefault')
                #en caso de que no existe, se asigna la licencia por defecto
                create = Rl_sucursal_licencia.objects.create(
                    fk_IdSucursal = reg,
                    fk_IdLicencia = licenciaasignada,
                    Fecha_vencimiento = fecha_vencimiento
                )
            response_data = {
                "message": "Sucursal creada y licencia asignada correctamente",
                "fecha_vencimiento": fecha_vencimiento,
                "sucursal": serializer_response.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='by-region', url_name='by-region')
    def get_sucursales_by_region(self, request):
        region_id = request.query_params.get('IdRegion')
        if not region_id:
            return Response({"error": "No se ha proporcionado una región"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sucursales = Sucursal.objects.filter(fk_IdRegion_id=region_id)
            if not sucursales.exists():
                return Response ({"mmesage": "No existen sucursales de este empresa"})
            lista_sucursales = []
            for sucursal in sucursales:
                sucursalserializado = sucursalSerializer(sucursal)
                querylicencia = Rl_sucursal_licencia.objects.filter(fk_IdSucursal = sucursal)
                if not querylicencia.exists():
                    infosucursales = {
                        'sucursal': sucursalserializado.data,
                        'licencias': 'null'
                    }
                    lista_sucursales.append(infosucursales)
                else:
                    licenciaserializada = licenciaSerializer(querylicencia, many=True)
                    infosucursales = {
                        'sucursal': sucursalserializado.data,
                        'licencias': licenciaserializada.data
                    }
                    lista_sucursales.append(infosucursales)
            serializer = sucursalSerializer(sucursales, many=True)
            return Response(lista_sucursales, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AreaViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Area_trabajo.objects.all()
    serializer_class = Area_trabajoSerializer
    
    @action(detail=False, methods=['post'], url_path='create-area', url_name='create-area')
    def createArea(self, request):

        serializer = Area_trabajoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Validar si ya existe una empresa con el mismo nombre
            nombre_zona = serializer.validated_data.get('Nombre_zona')
            idsucursal = request.data.get('fk_IdSucursal')
            
            try:
                querysucursal = Sucursal.objects.get(pk=idsucursal)
            except:
                return Response({"Error":"No existe la sucursal"}, status=status.HTTP_204_NO_CONTENT)
            if Area_trabajo.objects.filter(Nombre_zona=nombre_zona, fk_IdSucursal=idsucursal).exists():
                # Si ya existe una empresa con el mismo nombre, devolver un error
                return Response({'error': 'Ya existe una area con los mismos datos.'}, status=status.HTTP_400_BAD_REQUEST)
            #convertir y guardar modelo
            
            area = Area_trabajo.objects.create(
                Nombre_zona = nombre_zona,
                Is_active = True,
                fk_IdSucursal =querysucursal
            )
            area.save()
            serializer_response = Area_trabajoSerializer(area)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='get-area-by-sucursal', url_name='get-area-by-sucursal')
    def get_area_by_sucursal(self, request):
        idsucursal = request.query_params.get('IdSucursal')
        
        if not idsucursal:
            return Response({'error': 'Se requiere proporcionar el ID de la sucursal.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sucursal = get_object_or_404(Sucursal, pk=idsucursal)
            areas = Area_trabajo.objects.filter(fk_IdSucursal=sucursal)
            areaserializer = Area_trabajoSerializer(areas, many=True)
            lista_area = []
            for area in areaserializer.data:

                try:
                    querydispositivo = dispositivo.objects.get(IdArea = area.get('IdArea'))
                    dispositivoserializer = dispositivoSerializer(querydispositivo)

                    if dispositivoserializer.data:
                        querysensor = sensor.objects.filter(fk_IdDispositivo = querydispositivo)
                        sensorserializer = SensorSerializer(querysensor, many=True)
                        sensores=[]
                        for sensorindividual in sensorserializer.data:

                            queryregistro = register.objects.filter(fk_IdSensor = sensorindividual.get('IdSensor')).order_by('-created_at').first()
                            registro = RegisterSerializer(queryregistro)
                            hoy = timezone.now()
                            queryregistrohoy = register.objects.filter(created_at=hoy)
                            if queryregistrohoy.exists():

                                valormax = queryregistrohoy.order_by('-Valor').first()
                                valormaxsrializer = RegisterSerializer(valormax)
                                valormaximo = valormaxsrializer.data.get('Valor')

                                valormin = queryregistrohoy.order_by('Valor').first()
                                valorminserializer = RegisterSerializer(valormin)
                                valorminimo = valorminserializer.data.get('Valor')
                            else:
                                valormaximo = "#"
                                valorminimo = "#"
                                
                            registro_info = {
                                "sensor": sensorindividual.get('IdSensor'),
                                "tipo": sensorindividual.get('fk_IdTipo'),
                                "valor": registro.data.get('Valor'),
                                "Fecha_registro": registro.data.get('created_at'),
                                "valor_maximo": valormaximo,
                                "valor_minimo": valorminimo
                            }
                            # print(registro_info)
                            sensores.append(registro_info)
                        area_info = {
                            "IdArea": area.get('IdArea'),
                            "Nombre_zona": area.get('Nombre_zona'),
                            "sensores": sensores
                        }
                        lista_area.append(area_info)
                except:
                    area_info = {
                            "IdArea": area.get('IdArea'),
                            "Nombre_zona": area.get('Nombre_zona')
                        }
                    lista_area.append(area_info)
            return Response(lista_area, status=status.HTTP_200_OK)
        except Sucursal.DoesNotExist:
            return Response({'error': 'Sucursal no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)