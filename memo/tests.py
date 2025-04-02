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

class GetMemoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("memo-list")
        Memo.objects.create(text="メモ1")
        Memo.objects.create(text="メモ2")

    def test_get_memo_list(self):
        # urls.pyに定義したエンドポイントを自動で取得
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_memos(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_include_data(self):
        response = self.client.get(self.url)
        for memo in response.data:
            self.assertIn("text", memo) # textフィールドが存在するか
            self.assertIn("created_at", memo)
        texts = [memo["text"] for memo in response.data]
        self.assertIn("メモ1", texts)
        self.assertIn("メモ2", texts)

class UpdateMemoTests(TestCase):
    def setUp(self):
        # テスト用のAPIクライアントとテストデータを作成
        self.client = APIClient()
        self.memo = Memo.objects.create(text="元のメモ")
        self.url = reverse("memo-detail", kwargs={"pk": self.memo.id})

    def test_update_memo(self):
        # 有効なデータを送信するとメモが作成されるかをテストする
        updated_data = {'text': '更新テスト'}
        response = self.client.put(self.url, updated_data, format='json')
        # ステータスコードが201 Createdであることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # データベースの値が更新されたか確認
        self.memo.refresh_from_db()
        self.assertEqual(self.memo.text, updated_data["text"])

    def test_update_memo_not_found(self):
        # 存在しないメモを更新しようとすると404 Not Foundを返す
        url = reverse("memo-detail", kwargs={"pk": 9999}) # 存在しないID
        update_data = {"text": "存在しないメモ"}
        response = self.client.put(url, update_data, format="json")
        # ステータスコードが404 Not Foundであることを確認
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_empty_memo(self):
        data = {'text': ''}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # エラーメッセージが含まれていることを確認
        self.assertIn("text", response.data)
        self.assertIsNotNone(response.data["text"]) # エラーメッセージが含まれていること


