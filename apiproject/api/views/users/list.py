from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from ...models import User
from ...serializer import UserSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Lista todos os usuários cadastrados no sistema",
    responses={200: UserSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([permissions.IsAuthenticated, TokenHasScope])
def get_user(request):
    """
    Lista todos os usuários cadastrados no sistema.
    Requer escopo: read
    """
    if not request.auth.application.authorization_grant_type == 'client-credentials':
        return Response({"error": "Invalid grant type"}, status=400)
        
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data) 