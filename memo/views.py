from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Memo
from .serializers import MemoSerializer

class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all().order_by("-created_at")
    serializer_class = MemoSerializer

    def update(self, request, *args, **kwargs):
        memo = get_object_or_404(Memo, pk=kwargs["pk"])
        serializer = self.get_serializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # メモの削除処理
        memo = get_object_or_404(Memo, pk=kwargs["pk"])
        memo.delete()
        return Response({"message": "メモを削除しました"}, status=status.HTTP_204_NO_CONTENT)

