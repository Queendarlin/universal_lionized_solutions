import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Defines types of bonuses available for users
class BonusType(models.TextChoices):
    REFERRAL = 'REFERRAL', 'Referral Bonus'
    PERFORMANCE = 'PERFORMANCE', 'Performance Bonus'

# Represents a bonus awarded to a user
class Bonus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bonuses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=BonusType.choices)
    claimed = models.BooleanField(default=False)
    date_claimed = models.DateTimeField(null=True, blank=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} Bonus of {self.amount} for {self.user} - Claimed: {self.claimed}"

    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"
        ordering = ['-awarded_at']
