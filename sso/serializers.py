from rest_framework import serializers


class EmailTestSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    recipients = serializers.ListField(
        child=serializers.CharField(max_length=100))
