#(Auto-Create Wallet for New User)

# If a new user signs up, we don’t want to manually create a wallet for them
# So this runs automatically when a new user is created

from django.db.models.signals import post_save    # Trigger after user is saved
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet


# This function runs automatically *right after* a new User is created.
@receiver(post_save, sender=User)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    # created == True means "a new user was just created"
    if created:
        # Automatically create wallet with default balance = 0
        Wallet.objects.create(user=instance)
