from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.decorators import protected_resource
from ...models import User
from ...serializer import UserSerializer

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
@protected_resource(scopes=['read', 'write'])
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