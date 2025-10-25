#(Show Models in Admin Panel)

# This makes Wallet & Transaction visible at:
# 127.0.0.1:8000/admin

from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction

admin.site.register(Wallet)         # Show Wallet table
admin.site.register(Transaction)    # Show Transaction table
