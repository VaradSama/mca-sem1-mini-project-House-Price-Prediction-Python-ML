from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    input_features = models.JSONField()
    predicted_price = models.FloatField()
    model_version = models.CharField(max_length=20, default='v1')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.predicted_price} at {self.created_at}"
