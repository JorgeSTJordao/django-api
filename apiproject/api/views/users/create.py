from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.decorators import protected_resource
from ...models import User
from ...serializer import UserSerializer

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
@protected_resource(scopes=['write'])
def create_user(request):
    """
    Cria um novo usuário com os dados fornecidos.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 