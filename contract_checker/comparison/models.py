# models.py
from django.db import models

class Comparison(models.Model):
    previous_text = models.TextField()
    current_text = models.TextField()
    llm_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
