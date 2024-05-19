from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework import permissions
from apps.accounts.models import *
from apps.company.models import *
from apps.company.serializers import *
from .serializers import *
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .tasks import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from rest_framework.views import APIView
from .tokens import account_activation_token
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.company.models import *
from apps.company.serializers import *
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes=(permissions.AllowAny,)
    
    @action(detail=False, methods=['post'], url_path='create-user', url_name='create-user')
    # @permission_classes([AllowAny])
    @method_decorator(csrf_exempt)  # Desactiva CSRF para esta vista
    def create_user(self, request, *args, **kwargs):
        if request.data.get('company'):
            try:
                querycompany = company.objects.get(ClaveEmpresa = request.data.get('company'))
            except:
                return Response({"Error":"Clave de empresa invalida"},status=status.HTTP_204_NO_CONTENT)
        print("Request data:", request.data)
        serializer = createUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        if request.data.get('company'):
            try:
                querycompany = company.objects.get(ClaveEmpresa = request.data.get('company'))
                empresa = CompanySerializer(querycompany)
                print(empresa.data)
                created = Rl_user_company.objects.create(
                    fk_IdUsuario = user,
                    fk_IdEmpresa = querycompany
                )
            except:
                return Response({"Error":"No se encontró la empresa"},status=status.HTTP_400_BAD_REQUEST)
        
        # Ahora agregamos los grupos si están presentes en los datos
        groups = request.data.get('groups', [])
        for group_id in groups:
            try:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Group.DoesNotExist:
                return Response({"Error": f"El grupo con ID {group_id} no existe."}, status=status.HTTP_400_BAD_REQUEST)
        
        scheme = request.scheme
        host = request.get_host()
        # Construir la URL base
        base_url = f"{scheme}://{host}"
        # Send verification email using Celery
        domain = get_current_site(request).domain
        print(user)
        send_verification_email.delay(user.id, base_url)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['post'], url_path='get-user-by-company', url_name='get-user-by-company')
    def getUser_by_company(self, request):
        idempresa = request.data.get('IdEmpresa')
        name = request.data.get('username')
        queryuser = User.objects.get(username=name)
        user = UserSerializer(queryuser,context={'request': request})
        if not idempresa:
            return Response({"Error": "No se ha proporcionado una empresa"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryrelation = Rl_user_company.objects.filter(fk_IdEmpresa=idempresa).exclude(fk_IdUsuario=user.data.get('id'))
            if not queryrelation.exists():
                return Response({"Error": "No se encontraron usuarios para esta empresa"}, status=status.HTTP_404_NOT_FOUND)
            
            relaciones = Rl_company_userSerializer(queryrelation, many=True, context={'request': request})
            return Response(relaciones.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateAccount(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                print(settings.FRONTEND_SUCCESS_URL)
                return HttpResponseRedirect(settings.FRONTEND_SUCCESS_URL)  # Redirigir a una página de éxito de activación
            else:
                return Response({'error': 'El enlace de activación no es válido.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]