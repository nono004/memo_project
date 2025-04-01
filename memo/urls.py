from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemoViewSet

# ルーターを作成し、ViewSetを登録
router = DefaultRouter()
router.register(r'memos', MemoViewSet, basename='memo')

urlpatterns = [
    path('api/', include(router.urls)),
]