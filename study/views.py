from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from study.models import StudyModel
from study.serializer import StudySerializer


# ... existing code ...


class StudyListView(APIView):
    serializer_class = StudySerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = StudyModel.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(self.serializer_class(instance).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            assert isinstance(e, Exception)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 디테일 전용 뷰: 리스트 경로에서 PUT 폼이 노출되지 않도록 분리
class StudyDetailView(APIView):
    serializer_class = StudySerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        assert isinstance(pk, (int,)), "pk 타입이 예상과 다릅니다."
        study = StudyModel.objects.filter(pk=pk).first()
        if not study:
            return Response({'message': 'Study not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(study)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        study = StudyModel.objects.filter(pk=pk).first()
        if not study:
            return Response({'message': 'Study not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(study, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(self.serializer_class(updated).data, status=status.HTTP_200_OK)