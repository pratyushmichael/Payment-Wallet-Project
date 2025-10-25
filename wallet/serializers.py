# wallet/serializers.py

'''
Serializers convert Python objects → JSON
This is needed because APIs return data, not HTML.
'''

from rest_framework import serializers
from .models import Wallet, Transaction

# Serializer = translates model -> JSON
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']   # These fields will appear in JSON output


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'timestamp']
