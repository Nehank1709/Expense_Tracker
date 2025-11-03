from django.db import models

class CurrentBalance(models.Model):
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"Current Balance: {self.amount}"

# Create your models here.
class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], max_length=200)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}: {self.amount} on {self.created_at}"
