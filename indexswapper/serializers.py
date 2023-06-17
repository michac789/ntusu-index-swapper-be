import os
from rest_framework import serializers


class PopulateDatabaseSerializer(serializers.Serializer):
    admin_key = serializers.CharField(max_length=100)
    web_link = serializers.CharField(max_length=500)
    num_entry = serializers.IntegerField(min_value=0)

    def validate_admin_key(self, value):
        if value != os.environ.get('INDEXSWAPPER_ADMIN_KEY', '12345'):
            raise serializers.ValidationError('Invalid admin key!')
        return value
