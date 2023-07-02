from NTUSU_BE.utils import send_email
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from sso.permissions import IsSuperUser
from sso.serializers import EmailTestSerializer


class EmailTestView(CreateAPIView):
    serializer_class = EmailTestSerializer
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = EmailTestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(send_email(
                subject=serializer.validated_data['subject'],
                body=serializer.validated_data['body'],
                recipients=serializer.validated_data['recipients'],
            ))
