from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework import permissions
from apps.accounts.models import *
from apps.company.models import *
from apps.company.serializers import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]