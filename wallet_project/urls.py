"""
URL configuration for wallet_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   # include is needed for login/logout routes
# import the view we want to route to
from wallet.views import transfer_money, wallet_home, add_money, signup_page

from wallet.views import wallet_api, transactions_api


urlpatterns = [
    # Django admin site (built-in)
    path('admin/', admin.site.urls),

    # ✅ Built-in Authentication URLs (login, logout, password reset, etc.)
    # /accounts/login/
    # /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')),

    # ✅ Signup Page (our custom view)
    path('signup/', signup_page, name='signup'),

    # When user visits /transfer/, call the transfer_money view function
    # name="transfer_money" lets us refer to this URL elsewhere, e.g. {% url 'transfer_money' %}
    path('transfer/', transfer_money, name='transfer_money'),

    # Wallet Dashboard
    path('', wallet_home, name='wallet_home'),  
    
    # / → Dashboard          /transfer/ → Transfer page

    path('add-money/', add_money, name='add_money'),

    # API Endpoints
    path('api/wallet/', wallet_api, name='wallet_api'),
    path('api/transactions/', transactions_api, name='transactions_api'),
]
