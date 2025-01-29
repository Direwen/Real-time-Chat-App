from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'password']
        
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields=['id', 'username', 'email']