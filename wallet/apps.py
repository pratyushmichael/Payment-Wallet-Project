# (Register Signals with Django)
# Hey, make sure signals.py runs when the project starts.

from django.apps import AppConfig

class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet'

    # This runs when Django starts
    def ready(self):
        import wallet.signals   # Load the auto-wallet code
