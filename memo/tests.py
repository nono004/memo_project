from django.test import TestCase
from .models import Memo
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class MemoModelTests(TestCase):
    def test_save_text(self):
        memo = Memo(text="テストメモ")
        self.assertIs(memo.can_save(), True)
    def test_null_text(self):
        null_memo = Memo(text=None)
        self.assertIs(null_memo.can_save(), False)
    def test_save_created_at(self):
        memo = Memo(text="テストメモ2")
        memo.save()
        self.assertIs(memo.is_created_at_valid(), True)

class CreateMemoTests(TestCase):
    def setUp(self):
        # APIClientのインスタンスを作成
        self.client = APIClient()
        # ルーティング名で定義
        self.url = reverse("memo-list")

    def test_create_memo_api(self):
        # 有効なデータを送信するとメモが作成されるかをテストする
        data = {'text': 'テストメモ3'}
        response = self.client.post('/api/memos/', data, format='json')
        # ステータスコードが201 Createdであることを確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # レスポンスに'text'と'created_at'が含まれているか確認
        self.assertIn("text", response.data)
        self.assertIn("created_at", response.data)
        # レスポンスに含まれるtextがdataで定義したtextと同じか
        self.assertEqual(response.data["text"], data["text"])

        #データベースにメモが追加されたか確認
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        self.assertEqual(memo.text, data["text"])

    def test_create_empty_text_memo(self):
        # textが空の場合、エラーレスポンスを返す
        data = {'text': ""}
        response = self.client.post(self.url, data, format='json')

        # ステータスコードが400 Bad Requestであることを確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # エラーメッセージが含まれていることを確認
        self.assertIn("text", response.data)
        # 適切なエラーメッセージが含まれていることを確認
        self.assertIsNotNone(response.data["text"])

    def test_create_memo_response_fields(self):
        # 作成後のレスポンスに'text'と'created_at'が含まれているか確認
        data = {'text':'レスポンスチェック'}
        response = self.client.post(self.url, data, format='json')

        # ステータスコードが201 Createdであることを確認
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 必要なフィールドがレスポンスに含まれているか確認
        self.assertIn("text", response.data)
        self.assertIn("created_at", response.data)
        self.assertEqual(response.data["text"], data["text"])