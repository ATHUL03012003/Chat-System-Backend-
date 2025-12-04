from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom fields to token payload if you want
        token["email"] = user.email
        token["username"] = user.username

        return token

    def validate(self, attrs):
        # Override username to use email
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
