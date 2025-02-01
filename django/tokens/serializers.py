from rest_framework import serializers


class TokenSerializer(serializers.Serializer):

    code = serializers.CharField(required=True, allow_blank=False)

class RefreshTokenSerializer(serializers.Serializer):

    refresh_token = serializers.CharField(required=True, allow_blank=False)
