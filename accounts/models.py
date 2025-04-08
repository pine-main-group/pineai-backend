from django.db import models
from django.contrib.auth.models import User

class PlanChoices(models.TextChoices):
    BASIC = "basic", "Basic"
    STANDARD = "silver", "Silver"
    PREMIUM = "gold", "Gold"
    Platinum = "platinum", "Platinum"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(
        max_length=10,
        choices=PlanChoices.choices,
        default=PlanChoices.BASIC
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()}"
