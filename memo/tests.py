from django.test import TestCase
from .models import Memo

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