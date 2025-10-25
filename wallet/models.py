#(The Database Tables)
#This file defines the structure of what data we store

from django.db import models
from django.contrib.auth.models import User   # Built-in Django user accounts
# Django comes with a built-in User system (username, password, login, authentication, etc.) out-of-the-box.

# Each user gets one wallet → stores their current balance.
class Wallet(models.Model):
    # Links wallet to a user. One user → One wallet
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Stores the money. DecimalField is used for money (not float).
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # This is just how the wallet will appear in admin dashboard.
    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: ₹{self.balance}"


# Every money movement (credit/debit) is recorded here.
class Transaction(models.Model):
    # Each transaction is linked to a wallet
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    # How much money was added/removed
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Whether money came in or went out
    transaction_type = models.CharField(
        max_length=10,
        choices=(('credit', 'credit'), ('debit', 'debit'))
    )

    # Automatically store date/time of transaction
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional text like: "Added by user", "Sent to Rahul", etc.
    description = models.CharField(max_length=255, blank=True)

    # ✅ New line: unique reference ID for idempotency
    reference_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount} on {self.timestamp}"
