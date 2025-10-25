# STEP 3 — Implement Safe Balance Transfer Logic

# We’ll write a function that:

#         Checks if sender has enough balance

#         Deducts amount from sender’s wallet

#         Credits amount to receiver’s wallet

#         Creates transaction records for both sides

#         Ensures atomicity (if anything fails → nothing is partially done)

# This prevents:

#         Negative balance

#         Double spending

#         Corrupted balances


# Create your views here.
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction   # Helps us ensure the transfer is "all or nothing"
from .models import Wallet, Transaction
from django.contrib.auth.forms import UserCreationForm  # Built-in signup form

#APIs
from rest_framework.decorators import api_view  # allows us to make API functions
from rest_framework.response import Response     # lets us return JSON response
from .serializers import WalletSerializer, TransactionSerializer


# This function handles transferring money from the logged-in user to another user.
# The @login_required ensures that only logged-in users can use this.
@login_required
def transfer_money(request):

    # Get all users except the current logged-in user.
    # We need this for the dropdown list of possible receivers.
    users = User.objects.exclude(id=request.user.id)

    # If the page was submitted using POST → this means the user clicked "Send".
    if request.method == "POST":

        # receiver_username is taken from the HTML form field named "receiver"
        receiver_username = request.POST.get("receiver")

        # Convert entered amount (string) to Decimal (used for handling money)
        amount = Decimal(request.POST.get("amount"))

        # Sender is the currently logged in user
        sender = request.user

        # Find the User object of the receiver using the username they typed
        receiver = User.objects.get(username=receiver_username)

        reference_id = request.POST.get("reference_id")

        # ✅ Check if we have already processed this transfer
        if Transaction.objects.filter(reference_id=reference_id).exists():
            return redirect("wallet_home")  # Do nothing — prevent double-transfer



        # transaction.atomic ensures either ALL steps succeed or NONE happen.
        # This prevents issues like money debited but not credited.
        with transaction.atomic():

            '''Moved wallet fetching inside transaction.atomic()
               Lock works only inside the transaction'''

            # ✅ SELECT ... FOR UPDATE applies a *row-level lock*
            # This prevents two transfers from modifying the same wallet at the same time → prevents race conditions
            sender_wallet = Wallet.objects.select_for_update().get(user=sender)
            receiver_wallet = Wallet.objects.select_for_update().get(user=receiver)

            # Check if sender has enough money to send
            if sender_wallet.balance < amount:
                # If not enough money → show error and stop the transfer
                return render(request, "transfer.html", {
                    "users": users,
                    "error": "Insufficient balance — cannot complete transfer."
                })

            # 1) Deduct money from sender's wallet
            sender_wallet.balance -= amount
            sender_wallet.save()

            # Record sender's transaction as a "debit" (money going out)
            Transaction.objects.create(
                wallet=sender_wallet,
                amount=amount,
                transaction_type="debit",
                description=f"Sent to {receiver.username}",
                reference_id=reference_id   # ✅ Store idempotency key
            )

            # 2) Add money to receiver's wallet
            receiver_wallet.balance += amount
            receiver_wallet.save()

            # Record receiver's transaction as a "credit" (money coming in)
            Transaction.objects.create(
                wallet=receiver_wallet,
                amount=amount,
                transaction_type="credit",
                description=f"Received from {sender.username}",
                reference_id=reference_id   # ✅ Store idempotency key
            )

        # After successful transaction → go to wallet home (we'll build this later)
        # after a successful transfer, for now, just go back to the same form page
        return redirect("transfer_money")   # (was wallet_home earlier)

    # If user simply opens the page (GET request), show the form.
    return render(request, "transfer.html", {"users": users})


@login_required
def wallet_home(request):
    # Get the wallet of the logged-in user
    wallet = Wallet.objects.get(user=request.user)

    # Get their transaction history (newest first)
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')

    # Render the dashboard page and send wallet + transactions to it
    return render(request, "wallet_home.html", {
        "wallet": wallet,
        "transactions": transactions
    })


@login_required
def add_money(request):
    # Get logged-in user's wallet
    wallet = Wallet.objects.get(user=request.user)

    if request.method == "POST":
        # Convert input amount to Decimal (safe for money operations)
        amount = Decimal(request.POST.get("amount"))

        # Add to balance
        wallet.balance += amount
        wallet.save()

        # Record transaction (credit)
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="credit",
            description="Money added to wallet"
        )

        # Redirect back to dashboard
        return redirect("wallet_home")

    # If user just opened the page, show the form
    return render(request, "add_money.html")


def signup_page(request):
    """
    This view shows a Signup Form and creates a new User.
    Django automatically hashes the password and validates inputs.
    When the user is created, our signal in signals.py creates a Wallet for them.
    """
    if request.method == "POST":
        # When user submits the signup form
        form = UserCreationForm(request.POST)

        # Check if form is valid (Django handles username rules, password strength, etc.)
        if form.is_valid():
            form.save()  # ✅ This creates the new user in the database
            return redirect('login')  # After signup, go to login page
    else:
        # If it's a GET request, show an empty signup form
        form = UserCreationForm()

    # Render signup page and send "form" to it
    return render(request, "signup.html", {"form": form})



@api_view(['GET'])
def wallet_api(request):
    """
    This API returns the logged-in user's wallet balance in JSON format.
    """
    wallet = Wallet.objects.get(user=request.user)  # Find user's wallet
    serializer = WalletSerializer(wallet)  # Convert wallet object -> JSON
    return Response(serializer.data)  # Return JSON to client


@api_view(['GET'])
def transactions_api(request):
    """
    This API returns the logged-in user's transaction history in JSON format.
    """
    wallet = Wallet.objects.get(user=request.user)   # get user's wallet
    txns = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')  # newest first
    serializer = TransactionSerializer(txns, many=True)  # many=True because list of objects
    return Response(serializer.data)  # Return JSON list
