from django.db import models
from django.utils.timezone import now

# Create your models here.
class Memo(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text
    def can_save(self):
        return self.text is not None
    def is_created_at_valid(self):
        return self.created_at is not None and self.created_at <= now()
