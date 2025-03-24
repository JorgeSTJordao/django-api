from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializer import UserSerializer

# Create your views here.
@swagger_auto_schema(
    method='get',
    operation_description="Lista todos os usuários cadastrados no sistema",
    responses={200: UserSerializer(many=True)}
)
@api_view(['GET'])
def get_user(request):
    """
    Lista todos os usuários cadastrados no sistema.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Create an user
@swagger_auto_schema(
    method='post',
    operation_description="Cria um novo usuário no sistema",
    request_body=UserSerializer,
    responses={
        201: UserSerializer,
        400: 'Bad Request'
    }
)
@api_view(['POST'])
def create_user(request):
    """
    Cria um novo usuário com os dados fornecidos.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get'],
    operation_description="Retorna os detalhes de um usuário específico",
    responses={200: UserSerializer, 404: 'Not Found'}
)
@swagger_auto_schema(
    methods=['put'],
    operation_description="Atualiza um usuário específico",
    request_body=UserSerializer,
    responses={200: UserSerializer, 400: 'Bad Request', 404: 'Not Found'}
)
@swagger_auto_schema(
    methods=['delete'],
    operation_description="Remove um usuário específico",
    responses={204: 'No Content', 404: 'Not Found'}
)
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Gerencia operações em um usuário específico.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)