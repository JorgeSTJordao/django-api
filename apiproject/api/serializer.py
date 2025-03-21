from rest_framework import serializers
from .models import User

# Serializer: convert this model into a JSON or XML format
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # what model
        model = User 
        # what fields we are interested
        fields = '__all__' 
