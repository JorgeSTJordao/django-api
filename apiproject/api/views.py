from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

# Create your views here.

@api_view(['GET'])
def get_user(request):
    """
    Lista todos os usuários.
    
    Retorna uma lista com todos os usuários cadastrados no sistema.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Create an user
@api_view(['POST'])
def create_user(request):
    """
    Cria um novo usuário.
    
    Parâmetros:
    - name: Nome do usuário
    - email: Email do usuário
    - password: Senha do usuário
    """
    serializer = UserSerializer(data=request.data)
    # Is it a valid user
    if serializer.is_valid():
        serializer.save() # Request for the create(validate_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Recupera, atualiza ou deleta um usuário.
    
    Parâmetros:
    - pk: ID do usuário
    
    Métodos:
    - GET: Retorna os detalhes do usuário
    - PUT: Atualiza o usuário
    - DELETE: Remove o usuário
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