from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from indexswapper.serializers import PopulateDatabaseSerializer
from indexswapper.utils.scraper import populate_modules


class PopulateDatabaseView(GenericAPIView):
    serializer_class = PopulateDatabaseSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            populate_modules(
                serializer.validated_data['num_entry'],
                serializer.validated_data['web_link']
            )
            return Response({
                'success': 'Population completed!',
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
